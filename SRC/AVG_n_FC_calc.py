#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 20:02:38 2022

@author: samiha
"""

import pandas as pd
import numpy as np
from default_GenPathways import *
from utils import GrpCol
from utils_calc import get_ind

def assign_n_cols(df,efcoldf):
    ft_ll=efcoldf['fire type'].unique().tolist()
    for fire_type in  ft_ll:
        efcols= efcoldf['efcol'][efcoldf['fire type']==fire_type].tolist()
        ft_df=df[efcols]
        ncolName='N '+fire_type.replace(' ','_')
        for i in range(len(ft_df)):
            df.loc[i,ncolName]=len(df[efcols].iloc[i].dropna().values)
    return df


def get_avg_df(df,efcoldf):
        ft_ll=efcoldf['fire type'].unique().tolist()
        for fire_type in  ft_ll:
            efcols= efcoldf['efcol'][efcoldf['fire type']==fire_type].tolist()
            colName='AVG '+fire_type.replace(' ','_')
            df[colName]=df[efcols].T.mean()
        
        col_ll=GrpCol(df)[1]+GrpCol(df)[4]+GrpCol(df)[5]+['id']
        avgdf=df[col_ll]
        
        avgcol=GrpCol(avgdf)[4]
        pmvals=avgdf[avgcol][avgdf['pollutant category']=='PM'].mean().values.tolist()
        pmind=avgdf[avgdf['id']=='PM2.5'].index[0]
        avgdf.loc[pmind,'compound']='PM<2.5'
        avgdf.loc[pmind,'id']='PM<2.5'
        
        for i in range(len(avgcol)):
            avgdf.loc[pmind,avgcol[i]]=pmvals[i]
            
        total_pm_ind=set(avgdf[avgdf['pollutant category']=='PM'].index)-{pmind}
        
        avgdf=avgdf.drop(index=total_pm_ind)
        avgdf=avgdf.reset_index(drop=True)
        
        return avgdf

def test(lumpval,spec_ef_sum):
    max_val=lumpval+2.5*lumpval
    min_val=lumpval-2.5*lumpval
    if min_val<0:
        min_val=0
    if (spec_ef_sum<=max_val) and (spec_ef_sum>min_val) :
        return 'yes'
    else:
        return 'no'


def get_formula_multiple_lumpid(df):
    uf=df['formula'].unique().tolist()
    ff=[]
    for f in uf:
        aa=len(df[df['formula']==f][~df['id'].str.contains('InChI')])
        if aa>1:
            ff.append(f)
    return ff

def get_ind_list_sfc(sfc,formula):
    df=sfc[sfc['formula']==formula]
    lump_inds=df[~df['id'].str.contains('InChI')].index.tolist()
    lump_inds.append(len(df))
    
    ind_ll=[]
    for i in range(len(lump_inds)-1):
        ll=(np.arange(lump_inds[i],lump_inds[i+1])).tolist()
        ind_ll.append(ll)
    return ind_ll



def Get_fc_calc(fc,df):
    hid=pd.read_excel(pdb[0].split('pdb')[0]+'pdb_hatch15.xlsx')    
    uf=fc['formula'].unique().tolist()
    avgcols=GrpCol(df)[4]
    
    for i in range(len(uf)):
        formula=uf[i]
        lumpid=fc['id'][fc['formula']==uf[i]][~fc['id'].str.contains('InChI')][~fc['id'].isin(hid['id'])].values[0]
        specids=fc['id'][fc['formula']==uf[i]][~fc['id'].isin([lumpid])].tolist()
        
        for col in avgcols:
            lumpval=df[col][df['id']==lumpid].values[0]
            spec_ef_sum=df[col][df['id'].isin(specids)].sum()
            
            lumpind=df[df['id']==lumpid].index[0]
            spec_inds=df[df['id'].isin(specids)].index.tolist()
            
            if test(lumpval,spec_ef_sum)=='yes':
                for ind in spec_inds:
                    fc_val=df[col].iloc[ind]/spec_ef_sum
                    lump_ef_contribution=df[col].iloc[lumpind]*fc_val
                    ncol='N '+col.split(' ')[1]
                    n=df[ncol].iloc[ind]
                    df.loc[ind,col]=(lump_ef_contribution+df[col].iloc[ind]*n)/(n+1)
                    df.loc[lumpind,col]=np.nan
    return df


def fc_calc(df):
    fc=pd.read_excel(backend_db_dir+'fc_calc_simple.xlsx')
    sfc=pd.read_excel(backend_db_dir+'fc_calc_specific.xlsx')
    
    f_m_lids=get_formula_multiple_lumpid(sfc)
    
    fc2=sfc[~sfc['formula'].isin(f_m_lids)]
    sfc=sfc[sfc['formula'].isin(f_m_lids)].reset_index(drop=True)
    
    fc=fc.append(fc2).reset_index(drop=True)

    avgcols=GrpCol(df)[4]
    
    df=Get_fc_calc(fc,df)
    
    sfc_uf=sfc['formula'].unique().tolist()
    
    for i in range(len(sfc_uf)):
        formula=sfc_uf[i]
        ll=get_ind_list_sfc(sfc,formula)
        for k in range(len(ll)):
            sdf=sfc[sfc.index.isin(ll[i])]
            df=Get_fc_calc(sdf,df)
    
    df=df.drop(columns=GrpCol(df)[5])
    d_ind=set(df.index)-set(df[GrpCol(df)[4]].dropna(how='all').index)
    df=df.drop(index=d_ind)
    df=df.reset_index(drop=True)
    return df

