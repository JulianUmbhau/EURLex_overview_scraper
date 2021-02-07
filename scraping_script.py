#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:17:01 2021

@author: jj
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

#browser = webdriver.Firefox()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--remote-debugging-port=9222")

driver_path = '/usr/bin/chromedriver'

dc_codes = {"rolling_stock":2234,
            "rail_network":3430,
            "rail_transport":4514,
            "vehicle_on_rails":4657}



def scrape_links(search_term, driver_path, chrome_options):
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    
    ### HACK HACK - PUT IN DATA FILE
    dc_codes = {"rolling_stock": 2234,
                "rail_network": 3430,
                "rail_transport": 4514,
                "vehicle_on_rails": 4657}

    ####
    delay = 5
    dc_code = str(dc_codes[search_term])
    driver.get("https://eur-lex.europa.eu/search.html?DC_CODED="+ dc_code +"&SUBDOM_INIT=ALL_ALL&DTS_SUBDOM=ALL_ALL&DTS_DOM=ALL&lang=en&type=advanced&qid=1612306865594")
    try:
        element = WebDriverWait(driver,delay).until(EC.element_to_be_clickable((By.CLASS_NAME,"wt-cck-btn-add"))).click()
    except:
        print("ok")
    
    i=0
    
    # går igennem dokument en for en
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

search_term = "rail_transport"
df = scrape_links(search_term, driver_path, chrome_options)



df = pd.DataFrame()
for key in dc_codes.keys():
    print(key)
    search_term = key
    df_temp = scrape_links(search_term = search_term, driver_path=driver_path, chrome_options=chrome_options)
    df = df.append(df_temp)


link_list_path = "./link_list.csv"
df.to_csv(link_list_path)











# df = pd.read_csv(link_list_path, index_col=0)

# ### getting information on documents based on links
# chrome_options = Options()
# #chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--remote-debugging-port=9222")

# driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

# link_list_clean = []
# for link in link_list:
#     link_list_clean.append(link.split(":")[2])


# doc_date_list = []


# for link in link_list_clean:
#     driver.get(str("https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:" + link))
#     try:
#         element = WebDriverWait(driver,delay).until(EC.element_to_be_clickable((By.CLASS_NAME,"wt-cck-btn-add"))).click()
#         print("accepted")
#     except:
#         print("accept not found")
    
#     print(driver.find_element_by_xpath("//*[@class='panel-group']").find_element_by_xpath(".//*[@id='title']").text)
#     print("")
#     print(driver.find_element_by_id("PPDates_Contents").text)
#     doc_date_list.append(driver.find_element_by_id("PPDates_Contents").text)
#     print("")






# What other information is needed?    



# TODO hente metadata robust
# TODO gemme data i fil - csv
# TODO Se noter
# https://www.youtube.com/watch?v=ztbFY_kL4jI
# https://selenium-python.readthedocs.io/navigating.html
