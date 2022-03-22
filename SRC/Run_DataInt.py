#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:45:06 2022

@author: samiha
"""
import pandas as pd
import numpy as np
from default_GenPathways import *

from DataInt_mainFunc import *
from Merge_MultLumpCom import *
from Get_LumpCom_Spec import *
from utils import import_fc_dataset, sort_nmog

int_df=DataInt()   
nmogdf=Get_nmog(int_df)   

r_iddf=reduce_multiple_LumCom(nmogdf)[0]
iddf=reduce_multiple_LumCom(nmogdf)[1]

nmogdf=insert_rdf_nmogdf(nmogdf,r_iddf,iddf)

lc_spec_df=Get_LumCom_Spec(nmogdf)

nmogdf=sort_nmog(nmogdf,lc_spec_df)

import_fc_dataset(nmogdf,lc_spec_df)
#
igdf=sort_igdf(int_df)
pmdf=sort_pmdf(int_df)
mdf=igdf.append(nmogdf).append(pmdf)
mdf.to_excel(neiva_local_dir+'Data/Integrated_dataset.xlsx',index=False)
    

