#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 09:53:47 2022
@author: Samiha Shahid; If spot any bug please contact sbint003@ucr.edu. Thank you!
"""
'''
READ ME:
    This script uses scan functions to scan datatsets. If the checks do not show warning.
    It reports the datasets are clear. Then it cleans any unwanted space from the datasets.
    Reports the dataset is prepared if no warning.

'''

# Importing python library

from scan_clean_funcs import *
from pretty_table import *

df=pd.DataFrame()
checks=['Unwanted string','Duplicate id','Pollutant category']
result=[]

result.append(Scan_UnwantedString())
result.append(Scan_dupId())
result.append(check_pollutant_category_col())
result.append(CleanSpace_cell())
result.append(CleanSpace_ColName())


t=create_PrettyTable_col2(['Check','Output'],checks,result)

print('Data preperation-')
print(t)
if 'WARNING!' in result:
    print('Your datasets are not prepared. Please check again.')
if 'WARNING!' not in result:
    print('Your datasets are prepared!')

          