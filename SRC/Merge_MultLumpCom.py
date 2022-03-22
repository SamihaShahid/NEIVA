#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:38:36 2022
@author: Samiha Shahid
"""

'''
'''

import pandas as pd
import numpy as np
import pubchempy as pcp
import sys
from default_GenPathways import *

from utils import GrpFormula,AltName,GrpCol

def Get_lcid_df(f_spec_lc,df):
    hid=pd.read_excel(pdb[0].split('pdb')[0]+'pdb_hatch15.xlsx')    
    df=df[df['formula'].isin(f_spec_lc)].reset_index(drop=True)
    df=df[~df['id'].str.contains('InChI')]
    df=df[~df['id'].isin(hid['id'])]
    df=df.reset_index(drop=True)
    return df
        
def select_max_len_CompoundStr(com_ll,id_ll):
    len_ll=[]
    for com in com_ll:
        len_ll.append(len(com))
    selected_ind=len_ll.index(max(len_ll))
    selected_id=id_ll[selected_ind]
    return  selected_id  

def slc_iddf_Mult_lcid(iddf,formula):
    slc_id=[]
    for f in formula:
        com_ll=iddf['compound'][iddf['formula']==f].tolist()
        id_ll=iddf['id'][iddf['formula']==f].tolist()
        sl_id=select_max_len_CompoundStr(com_ll,id_ll)
        slc_id.append(sl_id)
    iddf=iddf[iddf['id'].isin(slc_id)]
    iddf=iddf.reset_index(drop=True)
    return iddf
    
def Mult_row2single_Row(df):
    uf=df['formula'].unique().tolist()
    efcols=GrpCol(df)[2]
    dfef=df[efcols+['formula']]
    
    ef_df=pd.DataFrame()
    for formula in uf:
        aa=pd.DataFrame(dfef[dfef['formula']==formula].mean()).transpose()
        ef_df=ef_df.append(aa)
    ef_df=ef_df.reset_index(drop=True)
    return ef_df

def reduce_multiple_LumCom(nmogdf):
    #formula with speciation and multiple lumped compound
    f_spec_multiple_lc=GrpFormula(nmogdf)[2]
    
    iddf=Get_lcid_df(f_spec_multiple_lc,nmogdf)
    #improting to backend_db
    iddf[GrpCol(iddf)[1]].to_excel(backend_db_dir+'nmog_MultLumCom.xlsx',index=False)
    
    slcdf=pd.read_excel(backend_db_dir+'nmog_MultLumCom_slc_no_rc.xlsx')[0].to_list()
    
    f_spec_multiple_lc=set(f_spec_multiple_lc)-set(slcdf)
    iddf=Get_lcid_df(f_spec_multiple_lc,nmogdf)
    
    slc_iddf=slc_iddf_Mult_lcid(iddf,f_spec_multiple_lc)
    
    slc_iddf=slc_iddf[GrpCol(slc_iddf)[1]+['id']]
    slc_iddf.to_excel(backend_db_dir+'nmog_MultLumCom_slc_id.xlsx',index=False)
    
    #changed compound name 
    df_altName=pd.read_excel(backend_db_dir+'nmog_MultLumCom_slc_id_altName.xlsx')
    slc_iddf=AltName(slc_iddf,df_altName)
    
    iddf_ef=Mult_row2single_Row(iddf)
    
    r_iddf=pd.concat([slc_iddf,iddf_ef],axis=1)
    r_iddf=r_iddf[GrpCol(r_iddf)[0]]
    
    return r_iddf, iddf    

def insert_rdf_nmogdf(nmogdf,rdf,df):
    nmogdf=nmogdf[~nmogdf['id'].isin(df['id'])]
    nmogdf=nmogdf.append(rdf).reset_index(drop=True)
    return nmogdf