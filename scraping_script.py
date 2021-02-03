#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:17:01 2021

@author: jj
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
for element in driver.find_element_by_xpath("//div[@class='SearchResult']").find_element_by_xpath(".//a[@class='title']"):
    

for element in driver.find_elements_by_xpath("//div[@class='SearchResult']"):
    print(element.text)
    break
for element in driver.find_elements_by_xpath("//div")

//*[@id="SearchCriteriaPanel"]/div/div/span[5]


//*[@id="MainContent"]/div[2]/div[2]/div/div[5]
# TODO Se noter
# https://www.youtube.com/watch?v=ztbFY_kL4jI
# https://selenium-python.readthedocs.io/navigating.html
