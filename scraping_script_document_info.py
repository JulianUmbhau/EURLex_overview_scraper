# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:21:21 2021

@author: jense
"""
# %%
from pandas.io.parsers import read_csv
import pandas as pd
import numpy as np
import functions

# %%
new_data = True
headless = False

link_list_path = "./link_list.csv"
link_list_full_path = "./link_list_full.csv"

# %%
chrome_options, driver_path = functions.set_chrome_options(headless)

# %%
### Kig på index!!
df = pd.read_csv(link_list_path, index_col=0)
df = df.reset_index().drop(columns="index")

# %%
if new_data:
    df["dates"] = "" # only if data is new
    df["categories"] = "" # only if data is new
    df["linked_docs"] = "" # only if data is new

# %%
df = functions.scrape_document_information(df, link_list_full_path, driver_path, chrome_options)
# %%
df.to_csv(link_list_full_path)

# %%
df = pd.read_csv(link_list_full_path, index_col=(0))

 # %%
df = functions.date_separation(df)
# %%
df = functions.category_separation(df)

# %%
df = functions.celex_separation(df)

# %%

df = functions.linked_docs_separation(df)



link_list_full_path_test = "link_list_full_test2.csv"
df.to_csv(link_list_full_path_test)

# %%
