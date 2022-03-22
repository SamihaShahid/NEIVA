#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 10:16:08 2022
@author: Samiha Shahid; If spot any bug please contact sbint003@ucr.edu. Thank you!
"""
'''
READ ME:
    This script has various functions that scans data.
'''

import pandas as pd
import numpy as np
import pubchempy as pcp

from selecting_db_dfs import *
from pretty_table import *


def Scan_UnwantedString():
   found_ll=[]
   file_list=bdb+rdb+pdb
   for file in file_list:
       data=pd.read_excel(file)
       found=[]
       for col in data.columns:
           for ind in range(len(data)):
               if '\ufeff' in str(data[col].iloc[ind]) :
                    found.append('yes')
               else:
                    found.append('no')
       ff=set(found)
       found_ll=found_ll+list(ff)
   if len(set(found_ll))==1 and 'no' in set(found_ll):
       return 'Clear'
   else:
       return 'WARNING!'

def Scan_dupId():
    file_list=bdb+rdb+pdb
    duplicated_id_files=['/Users/samiha/Desktop/NEIVA v 1.1/Data/base_db/temperate_forest.xlsx',
                       '/Users/samiha/Desktop/NEIVA v 1.1/Data/base_db/chaparral.xlsx',
                        '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_hatch15.xlsx',
                         '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_tmf_hatch17.xlsx',
                        '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_p_hatch17.xlsx',
                        '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_crr_hatch17.xlsx',
                       '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_bf_hatch17.xlsx']
    new_file_list=[]
    for file in file_list:
        data=pd.read_excel(file)
        data=data[data['id'].notna()].reset_index(drop=True)
        if len(data[data['id'].duplicated()])!=0:
            new_file_list.append(file)
    
    file_dup_id=list(set(new_file_list) - set(duplicated_id_files))
      
    if len(file_dup_id)==0:
        return 'Clear'
    if len(file_dup_id)>0:
        return ('WARNING!')


def check_pollutant_category_col():
   file_list=bdb+rdb+pdb
   unique_val_list=[]
   for file in file_list:
        data=pd.read_excel(file)
        unique_val_list=unique_val_list+list(data['pollutant category'].unique())
   unique_val_list=set(unique_val_list)
   aa=unique_val_list-{'NMOG',
                         'PM',
                         'PM optical property',
                         'PM speciation',
                         'PM speciation-carbon',
                         'PM speciation-ion',
                         'PM speciation-metal',
                         'PM speciation-organic species',
                         'PM speciation-organic species-PAH',
                         'PM speciation-organic species-anhydrosugar',
                         'PM speciation-organic species-branched alkane',
                         'PM speciation-organic species-hopane',
                         'PM speciation-organic species-lignin decomposition product',
                         'PM speciation-organic species-n alkane',
                         'PM speciation-organic species-sterol',
                         'PM speciation-organic species-sterol and stanol',
                         'PM speciation-organic species-tricyclic terpane',
                         'inorganic gas',
                         'methane',np.nan}
   if len(aa)==0:
       return 'Clear'
   if len(aa)>0:
       return 'WARNING!'

def check_inorganic_gas():
    ig_list=pd.read_excel(neiva_local_dir+'Source code/backend_db/list of inorganic gas.xlsx')
    ig_id_list=list(ig_list['id'])
    file_list=bdb+rdb+pdb
    found_ll=[]
    for file in file_list:
         data=pd.read_excel(file)
         data=data[data['pollutant category']=='inorganic gas'].reset_index(drop=True)
         data=data[~data['id'].isin(ig_id_list)]
         found=[]
         if len(data)>0:
             found.append('yes')
         if len(data)==0:
             found.append('no')
    ff=set(found)
    if len(ff)==1 and 'no' in ff:
        return 'Clear'
    if len(ff)==2 or 'yes' in ff:
        return 'WARNING!'
        


def CleanSpace_cell():
   file_list=bdb+rdb+pdb
   database=[]
   dataset=[]
   task_completion=[]
   for file in file_list:
        data=pd.read_excel(file)
        for col in data.columns:
            for ind in range(len(data)):
                if type(data[col][ind])==str:
                    data.loc[ind,col]=data[col][ind].strip()
        data.to_excel(file,index=False)
   return 'Unwanted space from cell cleaned.'


def CleanSpace_ColName():
   file_list=bdb+rdb+pdb
   for file in file_list:
        data=pd.read_excel(file)
        for col in data.columns:
            data=data.rename(columns={col:col.strip()})
   return 'Unwanted space from column header cleaned.'
        









