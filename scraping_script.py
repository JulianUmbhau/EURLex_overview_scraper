#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:17:01 2021

@author: jj
"""

from selenium.webdriver.chrome.options import Options
import pandas as pd
import data
import functions

#browser = webdriver.Firefox()

chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument("--remote-debugging-port=9222")

driver_path = '/usr/bin/chromedriver'

driver_path = "./chromedriver3.exe"

search_term = "rail_transport"
df = functions.scrape_links(search_term, driver_path, chrome_options)



df = pd.DataFrame()
for key in data.dc_codes.keys():
    print(key)
    search_term = key
    df_temp = functions.scrape_links(search_term = search_term, driver_path=driver_path, chrome_options=chrome_options)
    df = df.append(df_temp)


link_list_path = "./link_list.csv"
df.to_csv(link_list_path)



# TODO hente metadata robust
# TODO gemme data i fil - csv
# TODO Se noter
# https://www.youtube.com/watch?v=ztbFY_kL4jI
# https://selenium-python.readthedocs.io/navigating.html
