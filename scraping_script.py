#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:17:01 2021

@author: jj
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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



# går igennem dokument en for en
for element in driver.find_elements_by_xpath("//div[@class='SearchResult']"): 
    print(element.text)
    name = element.text
    element.click()
    driver.find_element_by_link_text("Document information").click()
    document_date = driver.find_elements_by_class_name("NMetadata").find_element_by_xpath("./dt['Date of document']/following-sibling::dd").text
    
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
