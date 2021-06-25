import pandas as pd
import numpy as np
   
# Reading the csv file
df_new = pd.read_csv('floridabar_extract.csv')
  
# saving xlsx file
GFG = pd.ExcelWriter('extract.xlsx')
df_new.to_excel(GFG, index = False)
  
GFG.save()