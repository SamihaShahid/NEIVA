#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 19:58:10 2022

@author: samiha
"""

import pandas as pd
import numpy as np
from default_GenPathways import *

def get_ind(intdf):
    com_df=pd.read_excel(backend_db_dir+'imp_comList_for_cacl.xlsx')
    co_ind=intdf[intdf['id']==com_df['id'][0]].index[0]
    co2_ind=intdf[intdf['id']==com_df['id'][2]].index[0]
    no_ind=intdf[intdf['id']==com_df['id'][1]].index[0]
    no2_ind=intdf[intdf['id']==com_df['id'][3]].index[0]
    return co_ind,co2_ind,no_ind,no2_ind

def correction_factor(intdf):
    co_ind=get_ind(intdf)[0]
    co2_ind=get_ind(intdf)[1]
   
    cfdf=pd.read_excel(backend_db_dir+'correction_factor.xlsx')
    
    iind=set(intdf.index)-{co_ind,co2_ind}
    
    for k in range(len(cfdf)):
        col=cfdf['efcol'].iloc[k]
        cf=cfdf['correction factor'].iloc[k]
        if col.find('koss18')!=-1:
            iind=set(intdf.index)-{co_ind,co2_ind}
        else:
            iind=intdf.index
            for i in iind:
                intdf.loc[i,col]=intdf[col].iloc[i]*cf
    return intdf
