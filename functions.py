# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:12:39 2021

@author: jense
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
import data


def scrape_links(search_term, driver_path, chrome_options):
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    
    dc_codes = data.dc_codes

    delay = 10
    dc_code = str(dc_codes[search_term])
    driver.get("https://eur-lex.europa.eu/search.html?DC_CODED="+ dc_code +"&SUBDOM_INIT=ALL_ALL&DTS_SUBDOM=ALL_ALL&DTS_DOM=ALL&lang=en&type=advanced&qid=1612306865594")
    try:
        element = WebDriverWait(driver,delay).until(EC.element_to_be_clickable((By.CLASS_NAME,"wt-cck-btn-add"))).click()
    except:
        print("Couldnt find")
    
    i=0
    
    # går igennem sider en for en
    df = pd.DataFrame(columns=("search_term", "title","link"))
                
    while True:
        
        try:
            driver.find_element_by_xpath("//*[@class='alert alert-info']")
            print("refreshing")
            driver.refresh()
            time.sleep(delay)
        except:
            pass
        urls = driver.find_elements_by_xpath("//*[@class='SearchResult']")
        for url in urls:
            temp = [str(search_term), 
                    url.find_element_by_xpath(".//*[@class='title']").text, 
                    url.find_element_by_xpath(".//*[@class='title']").get_attribute("name")]
            df.loc[len(df)] = temp
            i += 1
            print(i)
        next_page_btn = driver.find_elements_by_xpath("//a[@title='Next Page']")
        if len(next_page_btn) <1:
            print("no more pages left")
            break
        element = WebDriverWait(driver,delay).until(EC.element_to_be_clickable((By.XPATH,"//*[@title='Next Page']")))
        driver.execute_script("return arguments[0].scrollIntoView();", element)
        element.click()
    driver.close()
    return(df)


def scrape_document_information(df, link_list_full_path, driver_path, chrome_options):
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    
    start_idx = df.dates.last_valid_index()
    delay = 1
    if start_idx is None:
        idx = 0
    else:
        idx = start_idx
    for link in df.link[idx:]:
        doc_code = link.split("=")[1]
        
        link_full = "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=" + str(doc_code) + "&qid=1612306865594"
        print(str(idx) + " of " + str(len(df)))
        driver.get(link_full)
        try:
            driver.find_element_by_xpath("//*[@class='wt-cck-btn-add']").click()
        except:
            pass
        try:
            driver.find_element_by_xpath("//*[@class='alert alert-info']")
            print("refreshing")
            driver.refresh()
            time.sleep(delay)
        except:
            pass
        try:
            dates = driver.find_element_by_id("PPDates_Contents").text
            categories = driver.find_element_by_id("PPClass_Contents").text
            try:
                linked_docs = driver.find_element_by_id("PPLinked_Contents").text
            except:
                linked_docs = "Not found"
        except:
            print("refreshing")
            driver.refresh()
            time.sleep(10)
            try:
                dates = driver.find_element_by_id("PPDates_Contents").text
            except:
                dates = "Dates non_existent"
        df.at[idx, "dates"] = dates
        df.at[idx, "categories"] = categories
        df.at[idx, "linked_docs"] = linked_docs
        if (idx % 100) == 0:
            print("Saving data")
            df.to_csv(link_list_full_path)
        idx += 1
    driver.close()
    return(df)


def date_separation(df):
    df["doc_date"] = np.nan
    df["doc_end_date"] = np.nan
    for term in range(0, df.dates.last_valid_index()+1):
        if "Date of document" in df.dates.iloc[term]:
            temp = df.dates.iloc[term].replace(":",";").split("\n")
            if "Date" in temp[1]:
                temp[1] = temp[1].split(";")[0]
            df.at[term,"doc_date"] = temp[1]
        if "Date of end of validity" in df.dates.iloc[term]:
            if "No end date" in temp[-1]:
                df.at[term,"doc_end_date"] = "No end date"
            else:
                df.at[term,"doc_end_date"] = "".join(temp[-2:]).replace("\n","")
        else:
            pass
    return(df)