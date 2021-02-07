# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:21:21 2021

@author: jense
"""

from selenium.webdriver.chrome.options import Options
import pandas as pd
import functions

chrome_options = Options()
chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("start-maximized")
#chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument("--remote-debugging-port=9222")
driver_path = "./chromedriver3.exe"
link_list_path = "./link_list.csv"

df = pd.read_csv(link_list_path, index_col=0)
df["dates"] = "NA"

df = functions.scrape_document_information(df, driver_path, chrome_options)
link_list_full_path = "./link_list_full.csv"
df.to_csv(link_list_full_path)
