#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 20:36:23 2022
@author: Samiha Shahid; If spot any bug please contact sbint@ucr.edu. Thank you!
"""

'''
READ ME:
    
List of functions-

1) selecting_db_dfs(bdb,rdb,pdb) :-
    
    Asks the user to select databases for a task then takes input from user.
    It will keep asking to select databases from a user until a correct input in given. 
    Returns the file list of selected databases.
        
'''

from pretty_table import create_PrettyTable_col2

def get_database():
    list_col=['Database(DB) Name', 'Please type']
    col_list1=['Base DB', 'Raw DB', 'Primary DB', 'To select all 3 DBs']
    col_list2=['bdb', 'rdb', 'pdb', 'all']
    t=create_PrettyTable_col2(list_col,col_list1,col_list2)
    db_list = [None]
    while ~set(db_list).issubset(['bdb','pdb','rdb','all'])==-1:
        print('+---------------------------------------------------------------------------+')
        print('\nSelect Database for this task (You can select multiple databases)-\n')
        print(t)
        selected_databases=input('\nAn example Input (selecting 2 databases)- bdd,rdb\n\n')
        print('+---------------------------------------------------------------------------+')
        db_list = selected_databases.split(',')
        print('\nYou have Selected:', db_list,'\n')
    return db_list


def selecting_db_dfs(bdb,rdb,pdb):
    database_list=get_database()
    file_dir_list=[]    
    for database in database_list:
        if database in 'bdb':
            file_dir_list=file_dir_list+bdb
        if database in 'rdb':
            file_dir_list=file_dir_list+rdb
        if database in 'pdb':
            file_dir_list=file_dir_list+pdb
        if database in 'all':
            file_dir_list=bdb+rdb+pdb
    return file_dir_list
