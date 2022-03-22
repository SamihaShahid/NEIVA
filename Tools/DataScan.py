#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 11:39:20 2022
@author: Samiha Shahid; If spot any bug please contact sbint003@ucr.edu. Thank you!
"""

'''
READ ME:
    This script has various data scanning functions.
    
    List of Functions:
    All functions asks to select databases for the specific task and takes input from users.
        
        Scan_UnwantedString() - Scans and report if \ufeff is spotted in any cell.
        
        ScanCell(input_string) - Scans and report if input_string is found/not found in any cell.
        
        ScanCol(col,input_string) - Scans and report if input_string is spotted in the input column.
        
        Scan_dupId() - Reports files if duplicated id is spotted.
        
        ScanMolecule() - Scan a molecule in formula column and reports found/not found.
        
        ScanCompound() - Scan a compound in compound column and reports found/not found.
            
        ScanID(compound_iid) - Scan an id in compound column and reports found/not found.
        
        check_pollutant_category_col() - Checks the pollutant category column. It checks the categories. 
                                         Reports if any unmatched category is spotted.
        
        check_inorganic_gas() - Checks the pollutant category column. It matches the compounds.
                                Reports if any unmatched compound is spotted.
        
    
'''

import pandas as pd
import numpy as np
import pubchempy as pcp
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../SRC')))

from default_GenPathways import *
from selecting_db_dfs import *
from pretty_table import *


def Scan_UnwantedString():
   print('\nTask: Scan '+'ufeff'+'. Notify if found.')
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   database=[]
   dataset=[]
   output=[]
   for file in file_list:
        data=pd.read_excel(file)
        found=[]
        for col in data.columns:
            for ind in range(len(data)):
                if '\ufeff' in str(data[col].iloc[ind]) :
                    print('+------------------------------------+')
                    print('WARNING!')
                    print('Dataframe- '+file.split('/')[-1].replace('.xlsx',''))
                    print('Column- '+col)
                    print('index- '+str(ind))
                    print('+------------------------------------+')
                    found.append('yes')
                else:
                    found.append('no')
        ff=set(found)
        if  'yes' in ff:
            database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('Found')
        if len(ff)==1 and 'no' in ff:
            database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('Not found')
   col_list=['Database','Dataset','Output']
   t=create_PrettyTable_col3(col_list,database,dataset,output)
   print('Task complete:')
   print(t)
   return

def ScanCell(input_string):
   print('\nTask: Scan '+input_string+' .Notify if found.')
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   
   database=[]
   dataset=[]
   output=[]
   
   for file in file_list:
        data=pd.read_excel(file)
        found=[]
        for col in data.columns:
            for ind in range(len(data)):
                if input_string in str(data[col].iloc[ind]):
                    print('+---------------------------------------------------+')
                    print('FOUND!')
                    print('Dataframe- '+file.split('/')[-1].replace('.xlsx',''))
                    print('Column- '+col)
                    print('index- '+str(ind))
                    print('Cell with input string:'+data[col].iloc[ind])
                    print('+--------------------------------------------------+')
                    found.append('yes')
                else:
                    found.append('no')
        ff=set(found)
        if 'yes' in ff:
            database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('Found')
        if len(ff)==1 and 'no' in ff:
            database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('Not found')
   
   col_list=['Database','Dataset','Output']
   t=create_PrettyTable_col3(col_list,database,dataset,output)
   print('Task complete:')
   print(t)
   return

def ScanCol(col,input_string):
   print('\nTask: Scan '+input_string+' in '+col+' column. Notify if found.')
   
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   
   database=[]
   dataset=[]
   output=[]
   
   for file in file_list:
        data=pd.read_excel(file)
        if col in data.columns:
            data=data[data[col].notna()].reset_index(drop=True)
            data=data[data[col].str.contains(input_string)]
            if len(data)>0:
                database.append(file.split('/')[-2])
                dataset.append(file.split('/')[-1].replace('.xlsx',''))
                output.append('Found')
            if len(data)==0:
                database.append(file.split('/')[-2])
                dataset.append(file.split('/')[-1].replace('.xlsx',''))
                output.append('Not found')
   col_list=['Database','Dataset','Output']
   t=create_PrettyTable_col3(col_list,database,dataset,output)
   print('Task complete:')
   print(t)
   return


def Scan_dupId():
    print('\nTask: Scan datasets. Notify if a dataset has duplicate ID.')
    duplicated_id_files=['/Users/samiha/Desktop/NEIVA v 1.1/Data/base_db/temperate_forest.xlsx',
                       '/Users/samiha/Desktop/NEIVA v 1.1/Data/base_db/chaparral.xlsx',
                        '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_hatch15.xlsx',
                         '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_tmf_hatch17.xlsx',
                        '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_p_hatch17.xlsx',
                        '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_crr_hatch17.xlsx',
                       '/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_bf_hatch17.xlsx']
    new_file_list=[]
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    for file in file_list:
        data=pd.read_excel(file)
        data=data[data['id'].notna()].reset_index(drop=True)
        if len(data[data['id'].duplicated()])!=0:
            new_file_list.append(file)
    
    file_dup_id=list(set(new_file_list) - set(duplicated_id_files))
      
    if len(file_dup_id)==0:
        print('Task complete: All datasets checked. There are no duplicate IDs.')
    if len(file_dup_id)>0:
        print('WARNING!')
        print('The follwing datasets have duplicated ids-\n')
        print(file_dup_id)
    return
    
def ScanMolecule():
    print('\nTask: Searches a molecule in formula column.')
    print('Please type molecule-')
    molecule=input('Example input: Br\n')
    
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    
    database=[]
    dataset=[]
    formula=[]
    
    for file in file_list:
        data=pd.read_excel(file)
        if 'formula' in data.columns and len(data[data['formula'].notna()])>0:
            data=data[data['formula'].str.contains(molecule,na=False)].reset_index(drop=True)
            if len(data)>0:
                database.append(file.split('/')[-2])
                dataset.append(file.split('/')[-1].replace('.xlsx',''))
                formula.append(','.join(data['formula']))
            if len(data)==0:
                database.append(file.split('/')[-2])
                dataset.append(file.split('/')[-1].replace('.xlsx',''))
                formula.append('Not found')
    col_list=['Database','Dataset','Output']
    t=create_PrettyTable_col3(col_list,database,dataset,formula)
    print('Task complete:')
    print(t)
    return

# Todo: need to check. Do not handle if wrong compound name is input
def ScanCompound():
    compound_iid=[]
    while len(compound_iid)==0:
        ans=input('Type the compound name-\n')
        compound_iid=pcp.get_compounds(ans,'name')
    compound_iid=compound_iid[0].inchi
    
    print('\nTask: Search the compound and reports found/not found.')    
    
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    
    database=[]
    dataset=[]
    output=[]
    index=[]
    
    for file in file_list:
        data=pd.read_excel(file)
        if 'compound' in data.columns:
            ind=list(data[data['id']==compound_iid].index)
            if len(ind)==1:
                database.append(file.split('/')[-2].strip())
                dataset.append(file.split('/')[-1].strip().replace('.xlsx',''))
                output.append('found')
                index.append(str(ind[0]))
            if len(ind)==0:
                database.append(file.split('/')[-2].strip())
                dataset.append(file.split('/')[-1].strip().replace('.xlsx',''))
                output.append('Not found')
                index.append(np.nan)
    list_col=['Database','Dataset','Output','Index']
    t=create_PrettyTable_col4(list_col,database,dataset,output,index)
    print('Task complete:')
    print(t)
    return

def ScanID(compound_iid):
    print('\nTask: Search id and reports found/not found.')    
    
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    
    database=[]
    dataset=[]
    output=[]
    index=[]
    
    for file in file_list:
        data=pd.read_excel(file)
        if 'compound' in data.columns:
            ind=list(data[data['id']==compound_iid].index)
            if len(ind)==1:
                database.append(file.split('/')[-2].strip())
                dataset.append(file.split('/')[-1].strip().replace('.xlsx',''))
                output.append('found')
                index.append(str(ind[0]))
            if len(ind)==0:
                database.append(file.split('/')[-2].strip())
                dataset.append(file.split('/')[-1].strip().replace('.xlsx',''))
                output.append('Not found')
                index.append(np.nan)
    list_col=['Database','Dataset','Output','Index']
    t=create_PrettyTable_col4(list_col,database,dataset,output,index)
    print('Task complete:')
    print(t)
    return


def get_unique_val_col(col):
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   unique_val_list=[]
   for file in file_list:
        data=pd.read_excel(file)
        unique_val_list=unique_val_list+list(data[col].unique())
   final_unique_list=set(unique_val_list)
   return final_unique_list


def check_pollutant_category_col():
   print('\nTask: Checks pollutant category column. Reports unmatched category.') 
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   unique_val_list=[]
   for file in file_list:
        data=pd.read_excel(file)
        unique_val_list=unique_val_list+list(data['pollutant category'].unique())
   final_unique_list=set(unique_val_list)
   aa=final_unique_list-{'NMOG',
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
       print('Task complete:')
       print('pollutant category column is CLEAN!')
   if len(aa)>0:
       print('Task complete:')
       print('The unmatched category-')
       print(aa)

def check_inorganic_gas():
    print('\nTask: Check inorganic gas assignment. Reports the unmatched list.')
    ig_list=pd.read_excel(neiva_local_dir+'Source code/backend_db/list of inorganic gas.xlsx')
    ig_id_list=list(ig_list['id'])
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    database=[]
    dataset=[]
    output=[]
    for file in file_list:
         data=pd.read_excel(file)
         data=data[data['pollutant category']=='inorganic gas'].reset_index(drop=True)
         data=data[~data['id'].isin(ig_id_list)]
         if len(data)>0:
             print('+---------------------------------------------------------------------------+')
             print('Warning!')
             print(file.split('/')[-1].replace('.xlsx','')+' has assigned the following compound as inorganic gas'+'-')
             print(data['compound'][data['pollutant category']=='inorganic gas'][~data['id'].isin(ig_list['id'])])
             print('+---------------------------------------------------------------------------+')
             database.append(file.split('/')[-2].strip())
             dataset.append(file.split('/')[-1].replace('.xlsx',''))
             output.append('Unmatched compound found')
         if len(data)==0:
             database.append(file.split('/')[-2].strip())
             dataset.append(file.split('/')[-1].replace('.xlsx',''))
             output.append('No unmatched compound')
    if 'Unmatched compound found' not in output:
        list_col=['Database','Dataset','Output']
        t=create_PrettyTable_col3(list_col,database,dataset,output)
        print('Task complete:')
        print(t)
        return

def check_col(col):
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    for file in file_list:
        data=pd.read_excel(file)
        if col not in data.columns:
            print(file)

    

def drop_row(iid):
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    for file in file_list:
        data=pd.read_excel(file)
        ind=list(data[data['id']==iid].index)
        if len(ind)>0:
            print('Database- '+file.split('/')[-2])
            print('Dataset- '+file.split('/')[-1].replace('.xlsx',''))
            print('Index- ',ind)
            data=data.drop(index=ind)
            data.to_excel(file,index=False)

# check if there is null formula of NMOG compounds
def check_formula():
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    for file in file_list:
        data=pd.read_excel(file)
        data=data[data['pollutant category']=='NMOG'].reset_index(drop=True)
        if len(data[data['formula'].isnull()])>0:
            print(file.split('/')[-1].replace('.xlsx',''))
            print(data[['compound','id']][data['formula'].isnull()])

    







