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
new_data = False
headless = True

link_list_path = "./link_list_final.csv"
link_list_full_path = "./link_list_full_final.csv"

# %%
chrome_options, driver_path = functions.set_chrome_options(headless)

# %%
### Kig på index!!
df = pd.read_csv(link_list_path, index_col=0)


# %%
df = df.drop_duplicates(subset="link")
df = df.reset_index().drop(columns="index")

# %%
df = functions.scrape_document_information(df, link_list_full_path, driver_path, chrome_options, new_data)
# %%
df.to_csv(link_list_full_path)

# %%
df = pd.read_csv(link_list_full_path, index_col=(0))

 # %%
df = functions.date_separation(df)
# TODO wrong dates in date of effect
# %%
df = functions.category_separation(df)

# %%
df = functions.celex_separation(df)

# %%
df = functions.linked_docs_separation(df)

# %%
df = functions.extract_journal_categories(df)
#%%


import re
import datetime

df["doc_end_date"]
df["date_end_color"] = ""
for idx in range(0,len(df)):
    string = df["doc_end_date"].iloc[idx]
    present_date = datetime.datetime.today()
    if "No end date" in string:
        color = "Green"
    elif "Date of end of validity" in string and "Not known" not in string:
        end_date = string.split(";")[1]
        end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        if end_date < present_date:
            color = "Red"
        else:
            color = "Yellow"
    else:
        color = "None"
    df["date_end_color"].iloc[idx] = color

        


link_list_full_path_test = "link_list_full_final2.csv"
df.to_csv(link_list_full_path_test)

# TODO 3 fejlregistrerede dokumenter - løs til næste scrape/dokument behandling!
# %%

