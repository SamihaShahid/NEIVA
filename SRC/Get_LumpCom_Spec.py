#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:41:36 2022
@author: Samiha Shahid
"""
'''
'''

import pandas as pd
import numpy as np
import pubchempy as pcp
import sys

from default_GenPathways import *

from utils import AltName,GrpCol

def eliminate_general_terms(df):
    g_terms=pd.read_excel(backend_db_dir+'nmog_LumComName_general_terms.xlsx')[0].to_list()
    for i in g_terms:
        df=df[~df['compound'].str.contains(i,na=False)]
    return df

def add_Spec2lumCom(lcdf,nmogdf):
    lc_spec_df=pd.DataFrame()
    for i in range(len(lcdf)):
        llid=[]
        df=pd.DataFrame()
        ll=lcdf['compound'][i].split('+')
        for k in ll:
            try:
                c=pcp.get_compounds(k.strip(),'name')
                llid.append(c[0].inchi)
                print(k.strip(), 'Assigned id')
            except:
                print(k.strip(), 'Unable to assign id.')
        specdf=nmogdf[nmogdf['id'].isin(llid)]
        if len(specdf)==len(ll):
            print('ids found in nmogdf')
            df=lcdf[i:i+1].append(specdf)
            lc_spec_df=lc_spec_df.append(df)
    lc_spec_df=lc_spec_df.reset_index(drop=True)
    return lc_spec_df


def Get_LumCom_Spec(nmogdf):     
    com=[]
    for i  in range(len(nmogdf)):
        if nmogdf['compound'][i].find('+')!=-1:
            com.append(nmogdf['compound'].iloc[i])
        
    lcdf=nmogdf[nmogdf['compound'].isin(com)].reset_index(drop=True)
    # import to backend db
    lcdf[GrpCol(lcdf)[1]+['id']].to_excel(backend_db_dir+'nmog_LumpedCom.xlsx',index=False)
    #changed name
    df_altName=pd.read_excel(backend_db_dir+'nmog_LumpCom_altName.xlsx')
    lcdf=AltName(lcdf,df_altName)
    
    lcdf=eliminate_general_terms(lcdf)
    lcdf=lcdf.reset_index(drop=True)
    
    lc_spec_df=add_Spec2lumCom(lcdf,nmogdf)
    
    return lc_spec_df
