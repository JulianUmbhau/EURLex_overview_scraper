# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:21:21 2021

@author: jense
"""
# %%
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import functions

# %%

new_data = True
headless = None
OS = "ubuntu"
OS = None
chrome_options = Options() 
driver_path = "./chromedriver3.exe"

if OS == "ubuntu":
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver_path = '/usr/bin/chromedriver'
if headless:
    chrome_options.add_argument('--headless')

link_list_path = "./link_list.csv"
link_list_full_path = "./link_list_full.csv"


# %%
df = pd.read_csv(link_list_path, index_col=0)

if new_data:
    df["dates"] = np.nan # only if data is new
    df["categories"] = np.nan # only if data is new
    df["linked_docs"] = np.nan # only if data is new

df = functions.scrape_document_information(df, link_list_full_path, driver_path, chrome_options)
# %%
df.to_csv(link_list_full_path)

# %%
df = pd.read_csv(link_list_full_path, index_col=(0))

 # %%
df = functions.date_separation(df)
# %%
### cateogry separation
df["EUROVOC"] = np.nan
for idx in range(0, df.categories.last_valid_index()+1):
    EUROVOC_temp = df.categories.iloc[idx].replace("\n", " ").split(" ")
    if "Subject" in EUROVOC_temp:
        EUROVOC_descriptors = ", ".join(EUROVOC_temp[2:EUROVOC_temp.index("Subject")])
    else:
        EUROVOC_descriptors = ", ".join(EUROVOC_temp[2:])
    df.at[idx, "EUROVOC"] = EUROVOC_descriptors

# %% extract CELEX number
df["CELEX"] = np.nan
for idx in range(0, df.link.last_valid_index()+1):
    CELEX = df.link.iloc[idx].split(":")[2]
    df.at[idx, "CELEX"] = CELEX
# %%
for idx in range(0, df.linked_docs.last_valid_index()+1):
    link = df.linked_docs.iloc[idx]
    if "Amendment" in link:
        print(link)
    print("no amendment")
    break




# %%


df.EUROVOC.iloc[0]

# TODO asd


# using re module
import re
re.search("descriptor:(.*)Subject", df.categories.iloc[0].replace("\n"," ")).group(1)




### document links separation
df["links_to"] = np.nan
df["links_from"] = np.nan















df.to_csv(link_list_full_path)
