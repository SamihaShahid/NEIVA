#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 19:58:18 2022

@author: samiha
"""
import pandas as pd
import numpy as np
from default_GenPathways import *

from utils_calc import get_ind

def get_lab_study_avg(intdf,efcoldf):
    fire_type_ll=efcoldf['fire type'].unique().tolist()
    for ft in fire_type_ll:
        study_ll=efcoldf['study'][efcoldf['fire type']==ft].unique().tolist()
        df=pd.DataFrame()
        for study in study_ll:
            efcols=efcoldf['efcol'][efcoldf['fire type']==ft][efcoldf['study']==study][efcoldf['measurement type']=='lab'].to_list()
            if len(efcols)>1:
                newcol='EF '+ft.replace(' ','_')+'_'+study
                intdf[newcol]=intdf[efcols].T.mean()
                intdf=intdf.drop(columns=efcols)
                df['efcol']=[newcol]
                df['fire type']=[ft]
                df['study']=[study]
                df['measurement type']=['lab']
                efcoldf=efcoldf[~efcoldf['efcol'].isin(efcols)]
                efcoldf=efcoldf.append(df)
                efcoldf=efcoldf.reset_index(drop=True)
    return intdf, efcoldf



def er_adj(df,efcoldf):
    for fire_type in set(efcoldf['fire type'].unique())-{'peat'}:
        fl=pd.read_excel(backend_db_dir+'compound_flaming_combustion_type.xlsx')
        
        lab=efcoldf['efcol'][efcoldf['fire type']==fire_type][efcoldf['measurement type']=='lab'].tolist()
        field=efcoldf['efcol'][efcoldf['fire type']==fire_type][efcoldf['measurement type']=='field'].tolist()
        
        co_ind=get_ind(df)[0]
        co2_ind=get_ind(df)[1]
        
        fieldavg=df[field].T.mean()
        
        field_ind=set(fieldavg.dropna().index)
        
        for l in lab:
            lab_ind=set(df[l][df['pollutant category']!='PM optical property'].dropna().index)-{co2_ind,co_ind}
            iind=lab_ind.intersection(field_ind)
            
            fl_ind=set(df[df.index.isin(iind)][df['id'].isin(fl['id'])].index)
            sml_ind=iind-fl_ind
            
            for k in fl_ind:
                df.loc[k,l]=round((df[l].iloc[k]/df[l].iloc[co2_ind] + fieldavg.iloc[k]/fieldavg.iloc[co2_ind])/2 * fieldavg.iloc[co2_ind],4)
                
            for k in sml_ind:
                df.loc[k,l]=round((df[l].iloc[k]/df[l].iloc[co_ind] + fieldavg.iloc[k]/fieldavg.iloc[co_ind])/2 * fieldavg.iloc[co_ind],4)
            #changing col name in df and efcoldf    
            df=df.rename(columns={l:l+'_ER_ADJ'})
            alt_ind=efcoldf[efcoldf['efcol']==l].index
            efcoldf.loc[alt_ind,'efcol']=l+'_ER_ADJ'
    return df, efcoldf        
