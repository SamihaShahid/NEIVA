#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:24:21 2022

@author: Samiha Shahid
"""
'''

'''

import pandas as pd
from default_GenPathways import intdf_dir,backend_db_dir,neiva_local_dir
from utils_calc import correction_factor
from ER_ADJ_calc import get_lab_study_avg, er_adj
from AVG_n_FC_calc import assign_n_cols,get_avg_df,fc_calc

efcoldf=pd.read_excel(backend_db_dir+'pdb_all_efcol_info.xlsx')
cflaming=pd.read_excel(backend_db_dir+'compound_flaming_combustion_type.xlsx')

intdf=pd.read_excel(intdf_dir)
intdf=correction_factor(intdf)

df=get_lab_study_avg(intdf,efcoldf)[0]
efcoldf=get_lab_study_avg(intdf,efcoldf)[1]

assert len(df.columns[df.columns.str.contains('EF')])== len(efcoldf)

df=er_adj(df,efcoldf)[0]
df=assign_n_cols(df,efcoldf)

avgdf=get_avg_df(df,efcoldf)    
avgdf=fc_calc(avgdf)   
    
avgdf.to_excel(neiva_local_dir+'Data/Recomended_EF.xlsx',index=False)



















