"""
Created on Tue Mar  8 12:07:36 2022
@author: Samiha Shahid

    List of functions-
    
    DataInt() :- Outputs integrated dataset of all PDB datasets.
    
    sort_igdf(df) :- Returns sorted inorganic gas dataset.
                     Input- A dataset that has pollutant category column.
    
    sort_pmdf(df) :- Returns ordered particulate matter dataset. The order sequence is
                     stored in backend_db/pm_order_seq.xlsx file.
                     Input- A dataset that has pollutant category column.
    
    Get_igdf(df) :- Returns NMOG dataset of input dataset.
                    Input- A dataset that has pollutant category column.
"""

import pandas as pd
from default_GenPathways import *


from order_formula import *
from pretty_table import *

def DataInt():
    df=pd.DataFrame()
    idcols=['mm','formula','compound','pollutant category','id']
    df=pd.read_excel(pdb[0])
    for file in pdb[1:]:
        data=pd.read_excel(file)
        data_id=data[idcols]
        data_ef=data[data.filter(like='EF').columns.tolist()+['id']]
        unmatched=data_id[~data_id['id'].isin(df['id'])]
        df=df.append(unmatched)
        df=df.merge(data_ef,on='id',how='left')
        
    assert len(df[df['id'].duplicated()]) == 0
    assert len(df)==len(df[df.columns[df.columns.str.contains('EF',na=False)]].dropna(how='all'))
    
    df=OrderFormula(df)
    df=nominal_mm_calulator(df)
    
    t=create_PrettyTable_col2(['Check','Output'],['Duplicate IDs','Row with all NaNs','formula column'],['Clear','Clear','Cleaned'])
    print('\nData Integration process COMPLETE!')
    print(t)
    return df


def sort_igdf(df):
    igdf=df[df['pollutant category'].isin(['inorganic gas','methane'])]
    igdf=igdf.sort_values(by='mm').reset_index(drop=True)
    return igdf

def sort_pmdf(df):
    pm_arrange_seq=pd.read_excel(backend_db_dir+'pm_order_seq.xlsx')[0].to_list()
    pmdf=pd.DataFrame()
    for i in pm_arrange_seq:
        pmdf=pmdf.append(df[df['pollutant category']==i])
    return pmdf

def Get_nmog(df):
    nmogdf=df[df['pollutant category']=='NMOG']
    nmogdf=nmogdf.sort_values(by=['mm','formula','id']).reset_index(drop=True)
    return nmogdf


