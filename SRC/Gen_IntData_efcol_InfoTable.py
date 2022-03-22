#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 22:16:18 2022

@author: samiha
"""
'''

'''
import pandas as pd
from default_GenPathways import *


def Get_firetype(df):
    rdf=pd.read_excel(backend_db_dir+'/pdb_fuelType2fireType_info.xlsx')
    efcols=df.columns[df.columns.str.contains('EF')].tolist()
    efcoldf=pd.DataFrame()
    efcoldf['efcol']=efcols
    for i in range(len(rdf)):
        fuel=rdf['fuel type'].iloc[i]
        firetype=rdf['fire type'].iloc[i]
        for k in range(len(efcoldf)):
            ind_ll=efcoldf[efcoldf['efcol'].str.contains(fuel,na=False)].index.tolist()
            for ind in ind_ll:
                efcoldf.loc[ind,'fire type']=firetype
    
    rdf2=pd.read_excel(backend_db_dir+'/pdb_cookingfire_info.xlsx')
    
    if 'fire type' in efcoldf.columns:
        efcoldf1=efcoldf[efcoldf['fire type'].notna()].reset_index(drop=True)
        efcoldf2=efcoldf[efcoldf['fire type'].isnull()].reset_index(drop=True)
    else:
        efcoldf1=pd.DataFrame()
        efcoldf2=efcoldf
        
    for i in range(len(rdf2)):
        fuel=rdf2['stove type'].iloc[i]
        firetype=rdf2['fire type'].iloc[i]
        for k in range(len(efcoldf2)):
            ind_ll=efcoldf2[efcoldf2['efcol'].str.contains(fuel,na=False)].index.tolist()
            for ind in ind_ll:
                efcoldf2.loc[ind,'fire type']=firetype

    final_efcoldf=efcoldf1.append(efcoldf2)
    final_efcoldf=final_efcoldf.sort_values(by='fire type').reset_index(drop=True)
    return final_efcoldf


def single_fuel(df):    
    efcoldf_all=pd.DataFrame()
    for i in range(len(df)):
        efcol=[]
        ft=[]
        mt=[]
        efcoldf=pd.DataFrame()
        
        file=pdb[0].split('pdb')[0]+df['dataset'].iloc[i]+'.xlsx'
        data=pd.read_excel(file)
        fire_type=df['fire type'].iloc[i]
        measurement_type=df['measurement type'].iloc[i]
        
        efcol=(data.columns[data.columns.str.contains('EF',na=False)].tolist())
        
        for k in range(len(efcol)):
            ft.append(fire_type)
            mt.append(measurement_type)
        efcoldf['efcol']=efcol
        efcoldf['fire type']=ft
        efcoldf['measurement type']=mt
    
        efcoldf_all=efcoldf_all.append(efcoldf)
        efcoldf_all=efcoldf_all.reset_index(drop=True)
    return efcoldf_all



def multiple_fuel(df):
    efcoldf_all=pd.DataFrame()
    for i in range(len(df)):
        file=pdb[0].split('pdb')[0]+df['dataset'].iloc[i]+'.xlsx'
        data=pd.read_excel(file)
        measurement_type=df['measurement type'].iloc[i]
        efcoldf=Get_firetype(data)
        
        for k in range(len(efcoldf)):
            efcoldf.loc[k,'measurement type']=measurement_type
        
        efcoldf_all=efcoldf_all.append(efcoldf)
        efcoldf_all=efcoldf_all.reset_index(drop=True)
    return efcoldf_all
            
            
def multiple_fuel_specific_info_table(df):
    efcoldf_all=pd.DataFrame()
    for i in range(len(df)):
        infoTable=pd.read_excel(backend_db_dir+'/'+mf_infoTable['dataset'].iloc[0]+'_info.xlsx')
        infoTable=infoTable[['efcol','fire type','measurement type']]
        efcoldf_all=efcoldf_all.append(infoTable)
        efcoldf_all=efcoldf_all.reset_index(drop=True)
    return efcoldf_all
    


#__
pdb_info=pd.read_excel(backend_db_dir+'/pdb_all_dataset_info.xlsx')
pdb_info=pdb_info[~pdb_info['dataset'].str.contains('akagi')]

# multiple fuel
mf=pdb_info[pdb_info['fire type']=='multiple fuel'].reset_index(drop=True)
# single fuel
sf=pdb_info[~pdb_info['fire type'].isin(['multiple fuel','multiple fuel(has seperate info dataset)'])].reset_index(drop=True)
# has seperate info dataset
mf_infoTable=pdb_info[pdb_info['fire type']=='multiple fuel(has seperate info dataset)'].reset_index(drop=True)
        
df1=single_fuel(sf)
df2=multiple_fuel(mf)
df3=multiple_fuel_specific_info_table(mf_infoTable) 
akagidf=pd.read_excel(backend_db_dir+'/pdb_akagi_info.xlsx')   

fdf=pd.DataFrame()        
fdf=fdf.append(df1).append(df2).append(df3).append(akagidf)

fdf=fdf.sort_values(by=['fire type','measurement type','efcol'])
fdf=fdf.reset_index(drop=True)

# assign study column
for i in range(len(fdf)):
    fdf.loc[i,'study']=fdf['efcol'].iloc[i].split('_')[-1].strip()

fdf.to_excel(backend_db_dir+'/pdb_all_efcol_info.xlsx',index=False)

# check

efcol_ll=[]
for file in pdb:
    data=pd.read_excel(file)
    ll=data.columns[data.columns.str.contains('EF',na=False)].tolist()
    efcol_ll=efcol_ll+ll
    
assert len(efcol_ll)==len(fdf)



                









