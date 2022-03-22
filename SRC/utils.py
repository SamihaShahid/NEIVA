#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 19:40:04 2022
@author: Samiha Shahid
"""


import pandas as pd
import numpy as np
import pubchempy as pcp

from default_GenPathways import *
from order_formula import exact_mm_calulator


def GrpFormula(df):
    hid=pd.read_excel(pdb[0].split('pdb')[0]+'pdb_hatch15.xlsx')    
    all_formula=df['formula'].unique().tolist()
    
    f_no_spec=[]
    for f in all_formula:
        if len(df[df['formula']==f])==1:
            f_no_spec.append(f)
    
    f_spec=set(all_formula)-set(f_no_spec)
    
    f_spec_no_lc=[]
    for f in f_spec:
        aa=df[df['formula']==f]
        bb=aa[aa['id'].str.contains('InChI',na=False)]
        if len(aa)==len(bb):
            f_spec_no_lc.append(f)
    
    f_spec_lc=f_spec-set(f_spec_no_lc)
    
    f_spec_multiple_lc=[]
    for f in f_spec_lc:
        aa=df[df['formula']==f]
        aa=aa[~aa['id'].str.contains('InChI',na=False)]
        aa=aa[~aa['id'].isin(hid['id'].tolist())]
        if len(aa)>1:
             f_spec_multiple_lc.append(f)
        
    f_spec_one_lc=[]
    for f in f_spec_lc:
        aa=df[df['formula']==f]
        aa=aa[~aa['id'].str.contains('InChI',na=False)]
        aa=aa[~aa['id'].isin(hid['id'])]
        if len(aa)==1:
            f_spec_one_lc.append(f)
    
    return f_no_spec, f_spec, f_spec_multiple_lc, f_spec_one_lc 

def AltName(df,df_altName):
    iid=df_altName['id'][df_altName['altered name'].notna()].to_list()
    altname=df_altName['altered name'][df_altName['altered name'].notna()].to_list()
    for i in range(len(iid)):
        iind=df[df['id']==iid[i]].index
        df.loc[iind,'compound']=altname[i]
    return df

def GrpCol(df):
    identityCol=['mm','formula','compound','pollutant category']
    efcol=df.filter(like='EF').columns.tolist()
    avgcol=df.filter(like='AVG').columns.tolist()
    ncol=df.filter(like='N').columns.tolist()
    idcol=['id']
    arranged_col=identityCol+efcol+idcol
    return arranged_col, identityCol, efcol, idcol, avgcol, ncol

def import_fc_dataset(nmogdf,lc_spec_df):
    specific_fc_df=lc_spec_df[GrpCol(lc_spec_df)[1]+['id']]
    specific_fc_df.to_excel(backend_db_dir+'fc_calc_specific.xlsx',index=False)
    
    simple_fc=nmogdf[nmogdf['formula'].isin(GrpFormula(nmogdf)[3])]
    simple_fc=simple_fc[~simple_fc['formula'].isin(specific_fc_df['formula'].tolist())]
    
    simple_fc=simple_fc[GrpCol(simple_fc)[1]+['id']]
    simple_fc.to_excel(backend_db_dir+'fc_calc_simple.xlsx',index=False)
    return


def sort_nmog(nmogdf,lc_spec_df):
    hid=pd.read_excel(pdb[0].split('pdb')[0]+'pdb_hatch15.xlsx')
    
    nmogdf=nmogdf[~nmogdf['id'].isin(lc_spec_df['id'])]
    nmogdf_lc=nmogdf[~nmogdf['id'].str.contains('InChI')][~nmogdf['id'].isin(hid['id'])]
    h_non_inchi=nmogdf[~nmogdf['id'].str.contains('InChI')][nmogdf['id'].isin(hid['id'])]
    
    nmogdf=nmogdf[~nmogdf['id'].isin(nmogdf_lc['id'])]
    nmogdf=nmogdf[~nmogdf['id'].isin(h_non_inchi['id'])]
    
    nmogdf=nmogdf.append(nmogdf_lc).sort_values(by=['mm','formula','id'])
    nmogdf=nmogdf.append(lc_spec_df)
    nmogdf=nmogdf.append(h_non_inchi)
    nmogdf=nmogdf.sort_values(by=['mm','formula'])
    nmogdf=nmogdf.reset_index(drop=True)
    return nmogdf

def GenID(data):
    if 'exact_mass'  not in data.columns:
        data=exact_mm_calulator(data)

    for i in range(len(data)):
        try:
            c=pcp.get_compounds(data['compound'][i],'name')
            data.loc[i,'id']=c[0].inchi
        except:
            data.loc[i,'id']=np.nan
    
    iind=list(data[data['id'].isnull()].index)
    for ind in iind:
        data.loc[ind,'id']=str(data['exact_mass'].iloc[ind])+'_'+str(data['formula'].iloc[ind])
    
    test=data[~data['id'].str.contains('InChI')]
    if len(test[test['id'].duplicated()])==0:
        return data
    if len(test[test['id'].duplicated()])>0:
        duplicated_ids=list(test['id'][test['id'].duplicated()])
        for dupID in duplicated_ids:
            ll=len(data['id'][data['id']==dupID])
            ind=list(data['id'][data['id']==dupID].index)
            for j in range(ll):
                data.loc[ind[j],'id']=data['id'].iloc[ind[j]].split('_')[0]+j*'0'+'_'+data['id'].iloc[ind[j]].split('_')[1]
    return data