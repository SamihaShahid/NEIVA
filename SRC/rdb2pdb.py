#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 16:17:49 2021

@author: samiha
"""

import pandas as pd
import numpy as np
import pubchempy as pcp

# NEIVA Raw DB

dd=pd.read_excel('/Users/samiha/Desktop/NEIVA v 1.1/Data/raw_db/rdb_hatch15.xlsx')
dd=dd[dd['id'].notna()].reset_index(drop=True)

#_Clean class subclass
for i in dd[dd['class'].notna()].index:
    dd.loc[i,'class']=dd['class'][i].replace('_',' ').replace('n&s','N & S').replace('oxygenated hydrocarbon','oxygenated non-aromatics').replace('aromatic hydrocarbon','aromatics').replace('aliphatic hydrocarbons','aliphatics')
    dd.loc[i,'subclass']=dd['subclass'][i].replace('_',' ').replace('Sesquiterpenes','sesquiterpenes').replace('dbe','DBE')

dd['voc_type']=dd['class']+':-'+dd['subclass']

#_________________________Clean: Handle duplicate ids__________________________
dd[['compound','id']][dd['id'].duplicated()]
efcols=dd.columns[dd.columns.str.contains('EF')]
dup_ids=dd['id'][dd['id'].duplicated()].unique().tolist()

for item in dup_ids:
    ind=list(dd[dd['id']==item].index)
    print(ind)
    for col in efcols:
        if dd[col][dd['id']==item].sum()==0:
            dd.loc[ind[0],col]=np.nan
        else:
            dd.loc[ind[0],col]=dd[col][dd['id']==item].sum()
    dd=dd.drop(index=ind[1:]).reset_index(drop=True)

#_________________________________________________________________________________
list(dd[~dd.id.str.contains('InChI')]['compound'].unique())

# _Cadinene isomer : C15H24 : 2484.21_1.448 : including this compound in duplicates
ind=list(dd[dd['compound']=='Cadinene isomer'].index)
for i in ind:
    dd.loc[i,'id']=dd['id'][ind[0]]

#_ 4-Hexen-3-one isomer : C6H10O 
ind=list(dd[dd['compound']=='4-Hexen-3-one isomer'].index)
for i in ind:
    dd.loc[i,'id']=dd['id'][ind[0]]

#_ C6 Diketone isomer : C6H10O2
ind=list(dd[dd['compound']=='C6 Diketone isomer'].index)
for i in ind:
    dd.loc[i,'id']=dd['id'][ind[0]]

#_ Ethyl-benzofuran isomer : C10H10O
ind=list(dd[dd['compound']=='Ethyl-benzofuran isomer'].index)
for i in ind:
    dd.loc[i,'id']=dd['id'][ind[0]]

dup_ids=dd['id'][dd['id'].duplicated()].unique().tolist()

for item in dup_ids:
    ind=list(dd[dd['id']==item].index)
    print(ind)
    for col in efcols:
        if dd[col][dd['id']==item].sum()==0:
            dd.loc[ind[0],col]=np.nan
        else:
            dd.loc[ind[0],col]=dd[col][dd['id']==item].sum()
    dd=dd.drop(index=ind[1:]).reset_index(drop=True)

el_com=[]
ll=list(dd[~dd.id.str.contains('InChI')]['compound'].unique())
for item in ll:
    if len(dd[dd['compound']==item])==1:
        el_com.append(item)
 
#        
isomer_has_name=dd[dd['compound'].isin(el_com)]     # => reduced     
has_in=dd[dd.id.str.contains('InChI')] # ==> no reduction

# needs reduction =>
no_in=dd[~dd.id.str.contains('InChI')][~dd['id'].isin(isomer_has_name['id'])]

uf=list(no_in['formula'].unique())


#
efcols=no_in.columns[no_in.columns.str.contains('EF')]
for ff in uf:
    vc=list(no_in['voc_type'][no_in['formula']==ff].unique())
    ind=list(no_in[no_in['formula']==ff].index)
    # print(len(vc))
    if len(vc)==1:
        for col in efcols:
            if no_in[col][no_in['formula']==ff].sum()==0:
                no_in.loc[ind[0],col]=np.nan
            else:
                no_in.loc[ind[0],col]=no_in[col][no_in['formula']==ff].sum()
        no_in=no_in.drop(index=ind[1:]).reset_index(drop=True)
    if len(vc)==2:
        for col in efcols:
            if no_in[col][no_in['formula']==ff][:-1].sum()==0:
                no_in.loc[ind[0],col]=np.nan
            else:
                no_in.loc[ind[0],col]=no_in[col][no_in['formula']==ff][:-1].sum()
        no_in=no_in.drop(index=ind[1:-1]).reset_index(drop=True)
data=pd.concat([has_in,isomer_has_name,no_in]).reset_index(drop=True)
# _PC column_ :
data.loc[0,'pollutant category']='inorganic gas'
data.loc[1,'pollutant category']='inorganic gas'
for i in data[data['pollutant category'].isnull()].index:
    data.loc[i,'pollutant category']='NMOG'

data=data.drop(columns=['rt1', 'rt2','class', 'subclass','casid', 'h_id'])

data=data[['mm','formula','compound','pollutant category',
           'EF black_spruce', 'EF ponder_pine',
       'EF rice_straw', 'EF indonesian_peat','EF g_cutgrass','EF wiregrass','voc_type', 'id']]

#_Rename columns_
for col in efcols:
    data=data.rename(columns={col:col.replace('black_spruce','blackspruce').replace('ponder_pine','ponderosa_pine')+'_hatch15'})

#_Change the isomer to isomers_
for i in data['compound'][data['compound'].str.contains('isomer')].index:
    data.loc[i,'compound']=data['compound'][i]+'s'
    
data1=data[data['pollutant category']=='inorganic gas']
data2=data[data['pollutant category']=='NMOG']

data2=data2.sort_values(by=['mm','formula','voc_type']).reset_index(drop=True) 
        
fdata=data1.append(data2).reset_index(drop=True)

''' There are rows that doesn't have any EF value because 
EF gcutgrass and EF wiregrass is dropped.
 '''

efcols = fdata.columns [ fdata.columns.str.contains('EF') ]
ef_allnull_ind = set(fdata.index)-set(fdata[efcols].dropna(how='all').index)

fdata = fdata.drop(index=ef_allnull_ind )

fdata=fdata.reset_index(drop=True)

#_change isomer names
ii=set(fdata['compound'][fdata['compound'].str.contains('isomer')].index)
exclude_ind={188,273,337,400,401,446}
fii=ii-exclude_ind


fdata.to_excel('/Users/samiha/Desktop/NEIVA v 1.1/Data/primary_db/hatch15.xlsx',index=False)





































