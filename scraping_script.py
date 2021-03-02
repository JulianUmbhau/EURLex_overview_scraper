#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:17:01 2021

@author: jj
"""
# %%
from selenium.webdriver.chrome.options import Options
import pandas as pd
import data
import functions

# %%
new_data = True
headless = True

link_list_path = "./link_list_final.csv"

# %%
chrome_options, driver_path = functions.set_chrome_options(headless)

# %%
df = pd.DataFrame()
search_terms = list(data.dc_codes.keys())
for key in search_terms:
    print(key)
    search_term = key
    df_temp = functions.scrape_links(search_term = search_term, driver_path=driver_path, chrome_options=chrome_options)
    df = df.append(df_temp)


df.to_csv(link_list_path)

# %%
#### REMOVE DUPLICATES AFTER AREA SEARCH


# TODO hente metadata robust
# TODO gemme data i fil - csv
# TODO Se noter
# https://www.youtube.com/watch?v=ztbFY_kL4jI
# https://selenium-python.readthedocs.io/navigating.html
