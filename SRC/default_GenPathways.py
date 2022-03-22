#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 16:36:21 2022
@author: Samiha Shahid
"""


import glob
from pathlib import Path

# If a file is open at the background ~$ gets combined with the pathway string. 
# This function removes ~$ string from pathway string.
def solve_file_open_error(db_file_list):
        for i in range(len(db_file_list)):
            db_file_list[i]=db_file_list[i].replace('~$','')
        return db_file_list

def get_all_path():
    neiva_local_dir=Path('.').absolute().parents[0]
    base_db_dir=neiva_local_dir / 'Data/base_db/'
    bdb=glob.glob(str(base_db_dir)+"/*.xlsx")
    bdb=solve_file_open_error(bdb)
    raw_db_dir=neiva_local_dir / 'Data/raw_db/'
    rdb=glob.glob(str(raw_db_dir)+"/*.xlsx") 
    rdb=solve_file_open_error(rdb)
    primary_db_dir=neiva_local_dir / 'Data/primary_db/'
    pdb=glob.glob(str(primary_db_dir)+"/*.xlsx") 
    pdb=solve_file_open_error(pdb)
    
    backend_db_dir=neiva_local_dir / 'SRC/backend_db/'
    intdf_dir=neiva_local_dir / 'Data/Integrated_dataset.xlsx'
    return str(neiva_local_dir)+'/',bdb,rdb,pdb,str(backend_db_dir)+'/',str(intdf_dir)

neiva_local_dir,bdb,rdb,pdb,backend_db_dir,intdf_dir = get_all_path()

