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
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import pandas as pd

#browser = webdriver.Firefox()

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

#driver = webdriver.Chrome()

dc_codes = {"rail_network":3430,
            "rail_transport":4514}

code = "DC_CODED=" + str(dc_codes["rail_network"])

driver.get("https://eur-lex.europa.eu/search.html?"+ code +"&SUBDOM_INIT=ALL_ALL&DTS_SUBDOM=ALL_ALL&DTS_DOM=ALL&lang=en&type=advanced&qid=1612306865594")

driver.find_element_by_class_name("SearchResult").find_element_by_class_name("title")
driver.find_element_by_xpath("//div[@class='SearchResult']").find_element_by_xpath(".//a[@class='title']").text
driver.find_element_by_class_name("wt-cck-btn-add").click()

results = pd.DataFrame()

doc_date_end_list = []
doc_date_start_list = []
link_list = []
titles_list = []
i=0
delay = 3
# går igennem dokument en for en

while True:
    next_page_btn = driver.find_elements_by_xpath("//a[@title='Next Page']")
    if len(next_page_btn) <1:
        print("no more pages left")
        break
    else:
        urls = driver.find_elements_by_xpath("//*[@class='iUh30']")
        urls = [url.text for url in urls]
    
    
### Gå igennem searchresults loop og få title og name
    
        urls = driver.find_element_by_xpath("//*[@class='SearchResult']").find_elements_by_xpath(".//*[class='title']")
    
        titles_list.append(element.find_element_by_xpath(".//a[@class='title']").text)
        link_list.append(element.find_element_by_xpath(".//a[@class='title']").get_attribute('name'))

        print(urls)




    element = WebDriverWait(driver,5).until(expected_conditions.element_to_be_clickable((By.ID,'Next Page')))
    driver.execute_script("return arguments[0].scrollIntoView();", element)
    element.click()




for element in driver.find_elements_by_xpath("//div[@class='SearchResult']"): 
    i += 1
    print(i)
    titles_list.append(element.find_element_by_xpath(".//a[@class='title']").text)
    link_list.append(element.find_element_by_xpath(".//a[@class='title']").get_attribute('name'))
    
    link_list

    driver.find_element_by_class_name("title").click()    
    driver.find_element_by_link_text("Document information").click()
    document_date = driver.find_elements_by_class_name("NMetadata")
    document_date[0].text
    element_text = driver.find_element_by_id("PPDates_Contents").text
    element_text = element_text.split("\n")
    doc_date_start_list.append(element_text[0:2])
    doc_date_end_list.append(element_text[6:8])
    try:
        go_back_elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "PPDates_Contents")))
        go_back_elem.click()
        driver.back()
        driver.back()
    except TimeoutException:
        print("Error - too long")
    
    
    
    # går igennem metadata og extracter
for desc_list in driver.find_elements_by_class_name("NMetadata"):
        print(desc_list.text)
        test = desc_list
        #print(desc_list.find_element_by_xpath("./dt['Date of document']/following-sibling::dd").text)
    
    break


# kan beautifulsoup bruges?
import requests
response = requests.get("https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32020R2222&qid=1612306865594")
page = response.text
soup = BeautifulSoup(page, "html.parser")
print(soup.prettify())

# TODO hente metadata robust
# TODO gemme data i fil - csv
# TODO Se noter
# https://www.youtube.com/watch?v=ztbFY_kL4jI
# https://selenium-python.readthedocs.io/navigating.html
