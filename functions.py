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
import sys
import re
from selenium.webdriver.chrome.options import Options


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


def scrape_document_information(df, link_list_full_path, driver_path, chrome_options, new_data):
    driver = webdriver.Chrome(driver_path, options=chrome_options)

    df_full = pd.read_csv(link_list_full_path,  index_col=0)
    df = pd.merge(df_full, df, how="outer")

    if new_data:
        df["dates"] = "" # only if data is new
        df["categories"] = "" # only if data is new
        df["linked_docs"] = "" # only if data is new
        idx = df.index[df.dates == ""][0]  

    idx = df["dates"].last_valid_index()
    delay = 1
    for link in df.link[idx:]:
        doc_code = link.split("=")[1]
        
        link_full = "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=" + str(doc_code) + "&qid=1612306865594"
        print(str(idx) + " of " + str(len(df)))
        try:
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
            df.dates.loc[idx] = str(dates)
            df.categories.loc[idx] = str(categories)
            df.linked_docs.loc[idx] = str(linked_docs)
        except:
            dates = "Not loaded"
            categories = "Not loaded"
            linked_docs = "Not loaded"

            df.dates.loc[idx] = str(dates)
            df.categories.loc[idx] = str(categories)
            df.linked_docs.loc[idx] = str(linked_docs)
        if (idx % 100) == 0:
            print("Saving data")
            df.to_csv(link_list_full_path)
        idx += 1
    driver.close()
    return(df)


def set_chrome_options(headless):
    chrome_options = Options() 
    if sys.platform in "win32":
        driver_path = "./chromedriver3.exe"
    else:
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--remote-debugging-port=9222")
        driver_path = '/usr/bin/chromedriver'
    if headless:
        chrome_options.add_argument('--headless')
    return(chrome_options, driver_path)


def date_separation(df):
    df["doc_date"] = ""
    df["doc_end_date"] = ""
    df["doc_date_of_effect"] = ""
    if df.dates.isna().any():
        idx_end = df.dates.last_valid_index()+1
    elif any(df.dates == ""):
        idx_end = df.index[df.dates == ""][0]
    else:
        idx_end = len(df.dates)     
    for term in range(0, idx_end):
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
        if "Date of effect" in df.dates.iloc[term]:
            df.at[term,"doc_date_of_effect"] = "".join(temp[-2:]).replace("\n","")
        else:
            pass
    return(df)


def category_separation(df):
    df["EUROVOC"] = ""
    for idx in range(0, df.categories.last_valid_index()+1):
        EUROVOC_temp = df.categories.iloc[idx].replace("\n", " ").split(" ")
        if "Subject" in EUROVOC_temp:
            EUROVOC_descriptors = ", ".join(EUROVOC_temp[2:EUROVOC_temp.index("Subject")])
        else:
            EUROVOC_descriptors = ", ".join(EUROVOC_temp[2:])
        df.at[idx, "EUROVOC"] = EUROVOC_descriptors
    return(df)


def celex_separation(df):
    df["CELEX"] = ""
    for idx in range(0, df.link.last_valid_index()+1):
        CELEX = df.link.iloc[idx].split(":")[2]
        df.at[idx, "CELEX"] = CELEX
    return(df)


def linked_docs_separation(df):
    import re
    linked_docs_categories = ["repeal","corrected_by","corrigendum_to","implicit_repeal","completed_by","amended_by","amendment_to","consolidated", "affected_by"]
    for column in linked_docs_categories:
        df[str(column)] = ""
    for idx in range(0, df.linked_docs.last_valid_index()):
        df.at[idx, "repeal"] = ",".join(re.findall("Repeal (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "corrected_by"] = ",".join(re.findall("Corrected by (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "corrigendum_to"] = ",".join(re.findall("Corrigendum to (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "implicit_repeal"] = ",".join(re.findall("Implicit repeal (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "completed_by"] = ",".join(re.findall("Completed by (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "amended_by"] = ",".join(re.findall("Amended by (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "amendment_to"] = ",".join(re.findall("Amendment to (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "consolidated"] = ",".join(re.findall("Consolidated (.*)", df.linked_docs.iloc[idx]))
        df.at[idx, "affected_by"] = ",".join(re.findall("Affected by case: (.*) Instruments", df.linked_docs.iloc[idx].replace("\n"," ")))
    return(df)


def extract_journal_categories(df):
    df["journal_category"] = ""
    for idx in range(0, len(df["CELEX"])):
        url = df["CELEX"].iloc[idx]
        match = re.compile("[^\d]").search(url)
        if match is None:
            doc_type = "No character"
        else:
            doc_type = url[match.start()]
        df["journal_category"].iloc[idx] = doc_type
    return(df)
