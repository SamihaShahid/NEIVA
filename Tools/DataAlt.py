#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 11:56:02 2022
@author: Samiha Shahid; If spot any bug please contact sbint003@ucr.edu. Thank you!
"""

'''
READ ME:
    This script has various data replacing, altering and dropping functions.
    
    List of Functions:
    All functions asks to select databases for the specific task and takes input from users.
        
        ScanDel_UnwantedString() - Reports and deletes \ufeff from cells.
        
        ScanDel_Cell(input_string) - Reports and deletes input_string from cells.
                                     input_string = The string you want to scan in all cells.  
        
        CleanSpace_ColName() - Replaces unwanted space from column name.
        
        CleanSpace_cell() - Replaces unwanted space from cell.
        
        RepVal_by_Com(col, new_val) - Replaces a value from a colum with new_val. It asks to input a compound from users.
                                      col= The column you want to replace a value from
                                      new_val= The new value you want to replace with
        
        RepVal_by_id(col, new_val, iid) - Replaces a value from a column with new_val.
                                          col= The column you want to replace a value from
                                          new_val=The new value you want to replace with
                                          iid= The id of a compound. It will search this id and complete the task.
                                            
        
        altid(old_id,new_id) - Replaces old_id with new_id.
                               old_id= The id you want to alter.
                               new_id= The id you want to alter with.
        
        RepVal_from_col(col, val_list, altered_val_list) - Replaces a value from a column with another value.
                                                           val_list= The list of value you want to change
                                                           altered_val_list= The list of alvalue you want to alter with
        
        DropCol(col) - Drops column from selected dataframes.
                       col= The column you want to drop.


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

#\ufeff
                        
def ScanDel_UnwantedString():
   print('\nTask: Scan and delete Unwanted string from cell.') 
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   for file in file_list:
        data=pd.read_excel(file)
        for col in data.columns:
            for ind in range(len(data)):
                if '\ufeff' in str(data[col].iloc[ind]) :
                    print('+------------------------------------------------------+')
                    print('WARNING!')
                    print('Dataframe- '+file.split('/')[-1].replace('.xlsx',''))
                    print('Column- '+col)
                    print('index- '+str(ind))
                    print('Cell with [unwanted string]:'+data[col].iloc[ind])
                    print('+------------------------------------------------------+')
                    data.loc[ind,col]=data[col].iloc[ind].replace('\ufeff','')                    
                    data.to_excel(file,index=False)
                    check_changed_data=pd.read_excel(file)
                    print('Deleted [unwanted string]:'+ check_changed_data[col].iloc[ind])
   print('Task complete!')
   return

def ScanDel_Cell(input_string) :
   print('\nTask: Scan and delete '+input_string+' from cell.') 
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   for file in file_list:
        data=pd.read_excel(file)
        for col in data.columns:
            for ind in range(len(data)):
                if input_string in str(data[col].iloc[ind]):
                    print('+--------------------------------------------+')
                    print('FOUND!')
                    print('Dataframe- '+file.split('/')[-1].replace('.xlsx',''))
                    print('Column- '+col)
                    print('index- '+str(ind))
                    print('Cell with [input String]:'+data[col].iloc[ind])
                    print('+--------------------------------------------+')
                    data.loc[ind,col]=data[col].iloc[ind].replace(input_string,'')                    
                    data.to_excel(file,index=False)
                    check_changed_data=pd.read_excel(file)
                    print('Deleted [input string]:'+ check_changed_data[col].iloc[ind])
   print('Task complete!')


def CleanSpace_ColName():
   print('\nTask: Remove Unwanted space from column header.')
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   database=[]
   dataset=[]
   task_completion=[]
   for file in file_list:
        data=pd.read_excel(file)
        for col in data.columns:
            data=data.rename(columns={col:col.strip()})
        data.to_excel(file,index=False)
        database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
        dataset.append(file.split('/')[-1].replace('.xlsx',''))
        task_completion.append('Yes')
   col_list=['Database','Dataset','Task completion']
   t=create_PrettyTable_col3(col_list,database,dataset,task_completion)
   print('Unwanted space from column header Cleaned!')
   print(t)
   return
        

def RepStr_ColName(input_string,replace_string):
   print('\nTask: Replace '+str(input_string)+' from column header.')
   
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   database=[]
   dataset=[]
   task_completion=[]
   for file in file_list:
        found=[]
        data=pd.read_excel(file)
        for col in data.columns:
            if input_string in col:
                found.append('yes')
                print('+------------------------------------------------------------------------+')
                print('FOUND!')
                print('Column with [input string]- '+col)
                data=data.rename(columns={col:col.replace(input_string,replace_string)})
                print('Replaced [input string]- '+data.columns[data.columns.isin([col.replace(input_string,replace_string)])][0])
                print('+-------------------------------------------------------------------------+')
            else:
                found.append('no')
        data.to_excel(file,index=False)
        ff=list(set(found))
        if len(ff)==1 and 'yes' in ff:
            database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            task_completion.append('Y')
        if len(ff)==1 and 'no' in ff:
            database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            task_completion.append('NOT FOUND!')
        if len(ff)==2:
            database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            task_completion.append('Y')
   df=pd.DataFrame()
   df['database']=database
   df['dataset']=dataset
   df['tc']=task_completion
   if len(df[df['tc']=='YES'])>0:
       df=df[df['tc']=='YES'].reset_index(drop=True)
       col_list=['Database','Dataset','Task completion']
       t=create_PrettyTable_col3(col_list,list(df['database']),list(df['dataset']),list(df['tc']))
       print('Task: Replacing '+input_string+' from column header')
       print(t)
   if len(df[df['tc']=='YES'])==0:
       print('All datasets checked. '+input_string+' NOT FOUND!')
   return


def CleanSpace_cell():
   print('\nTask: Remove Unwanted space from cell.') 
   file_list=selecting_db_dfs(bdb,rdb,pdb)
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
        database.append(file.split('/')[-2].replace('base_db','Base DB').replace('raw_db','Raw DB').replace('primary_db','Primary DB'))
        dataset.append(file.split('/')[-1].replace('.xlsx',''))
        task_completion.append('Yes')
   col_list=['Database','Dataset','Task completion']
   t=create_PrettyTable_col3(col_list,database,dataset,task_completion)
   print('Unwanted space in cell CLEANED!')
   print(t)
   return


def RepVal_by_ComName(col, new_val):
   compound_iid=[]
   
   while len(compound_iid)==0:
       ans=input('Type the compound name-\n')
       compound_iid=pcp.get_compounds(ans,'name')
   
   compound_iid=compound_iid[0].inchi
   
   print('\nTask: '+'Insert '+str(new_val)+' in '+col+' column'+' where compound is '+ans)
   
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   database=[]
   dataset=[]
   task_status=[]
   for file in file_list:
        data=pd.read_excel(file)
        if col in data.columns:
            ind=data[col][data['id']==compound_iid].index
            if len(ind)==1:
                data.loc[ind,col]=new_val
                data.to_excel(file,index=False)
                database.append(file.split('/')[-2].strip())
                dataset.append(file.split('/')[-1].replace('.xlsx',''))
                task_status.append('Found and replaced')
            if len(ind)==0:
                database.append(file.split('/')[-2].strip())
                dataset.append(file.split('/')[-1].strip().replace('.xlsx',''))
                task_status.append('Not found')
   col_list=['Database','Dataset','Task status']
   t=create_PrettyTable_col3(col_list,database,dataset,task_status)
   print('Task complete:')
   print(t)          
   return

def RepVal_by_id(col, new_val, iid):
   print('\nTask: '+'Insert '+str(new_val)+' in '+col +' column'+'where id is'+iid)
   
   file_list=selecting_db_dfs(bdb,rdb,pdb)
   database=[]
   dataset=[]
   task_status=[]
   
   for file in file_list:
        data=pd.read_excel(file)
        if col in data.columns:
            ind=data[col][data['id']==iid].index
            if len(ind)==1:
                data.loc[ind,col]=new_val
                data.to_excel(file,index=False)
                database.append(file.split('/')[-2])
                dataset.append(file.split('/')[-1].replace('.xlsx',''))
                task_status.append('ID found and replaced')
            if len(ind)==0:
                database.append(file.split('/')[-2])
                dataset.append(file.split('/')[-1].replace('.xlsx',''))
                task_status.append('ID not found')
   col_list=['Database','Dataset','Task status']
   t=create_PrettyTable_col3(col_list,database,dataset,task_status)
   print('Task complete:')
   print(t)
   return


def altid(old_id,new_id):
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    database=[]
    dataset=[]
    output=[]    
    for file in file_list:
        data=pd.read_excel(file)
        ind=data[data['id']==old_id].index
        if len(ind)==1:
            data.loc[ind,'id']=new_id
            data.to_excel(file,index=False)
            database.append(file.split('/')[-2].strip())
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('Changed id')
        if len(ind)==0:
            database.append(file.split('/')[-2].strip())
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('id not found')
    list_col=['Database','Dataset','Output']
    t=create_PrettyTable_col3(list_col,database,dataset,output)
    print('Task complete:')
    print(t)
    return

        
def RepVal_from_col(col, val_list, altered_val_list):
       file_list=selecting_db_dfs(bdb,rdb,pdb)
       for file in file_list:
           data=pd.read_excel(file)
           for i in range(len(val_list)):
               iindex=list(data[data[col]==val_list[i]].index)
               if len(iindex)>0:
                   print('dataset-'+' '+file.split('/')[-1].replace('.xlsx',''))
                   print('\n')
                   print(data[col][data.index.isin(iindex)])
                   print('\n')
                   for ind in iindex:
                       data.loc[ind,col]=changed_val_list[i]

                   data.to_excel(file,index=False)
                   data=pd.read_excel(file)
                   print('changed value-')
                   print(data[col][data.index.isin(iindex)])
             
def DropCol(col):
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    database=[]
    dataset=[]
    output=[]
    for file in file_list:
        data=pd.read_excel(file)
        if col in data.columns:
            # data=data.drop(columns=[col])
            # data.to_excel(file,index=False)
            database.append(file.split('/')[-2].strip())
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('Column deleted')
        else:
            database.append(file.split('/')[-2].strip())
            dataset.append(file.split('/')[-1].replace('.xlsx',''))
            output.append('Column not found')
    list_col=['Database','Dataset','Output']
    t=create_PrettyTable_col3(list_col,database,dataset,output)
    print('Task complete:')
    print(t)
    return
    

# need to check this function   
def rep_colName(input_str,alt_string):
    file_list=selecting_db_dfs(bdb,rdb,pdb)
    fdf=pd.DataFrame(file_list)
    ans=input('select a dataset for this task-\n')
    file_ind=fdf[fdf[0].str.contains(ans,na=False)].index.tolist()[0]
    print(fdf[0].iloc[file_ind])
    ans2=input('Is the dataset correct-\n')
    if ans2=='yes':
        file=fdf[0].iloc[file_ind]
        df=pd.read_excel(file)
        old_col=df.columns[df.columns.str.contains(input_str)].tolist()[0]
        print('Old Col- '+ old_col)
        ans3=input('Correct-\n')
        if ans3=='yes':
            new_col=old_col.replace(input_str,alt_string)
            print('New col- '+ new_col)
            ans4=input('Correct\n')
            if ans4=='yes':
                df=df.rename(columns={old_col:new_col})
                df.to_excel(file,index=False)
        
        
def read_table():
   aa=pd.DataFrame(pdb)
   dataset=[]
   for dt_pathway in pdb:
       dataset.append(dt_pathway.split('/')[-1].replace('.xlsx',''))   
   print(dataset)
   ans=input('select a table\n')
   ind=aa[aa[0].str.contains(ans,na=False)].index.tolist()[0]
   slc_pathway=aa[0].iloc[ind]
   data=pd.read_excel(slc_pathway)
   return data
   
    
 
        
    
    

    
    
    
    
    
    
    














