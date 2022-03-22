#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 19:32:34 2022
@author: Samiha Shahid
"""
'''

'''
import pandas as pd
import numpy as np

from default_GenPathways import *
from pretty_table import *

def Get_molec_formula():
    file_list=bdb+rdb+pdb
    ss=''
    for file in file_list:
        data=pd.read_excel(file)
        if 'formula' in data.columns:
            data=data[data['formula'].notna()]
            data=data[~data['id'].isin(['NOx_as_NO'])]
            data=data[data['pollutant category'].isin(['inorganic gas','NMOG'])]
            data=data.reset_index(drop=True)
            for k in range(len(data)):
                ss=ss+ data['formula'][k]
    ll=set(ss)-{'1','2','3','4','5','6','7','8','9','0'}
    ll=list(ll)
    if 'B' in ll and 'r' in ll:
        ll.remove('B')
        ll.remove('r')
        ll.append('Br')
    if 'l' in ll and 'C' in ll:
        ll.remove('l')
        ll.append('Cl')
    if 'L' in ll and 'C' in ll:
        ll.remove('L')
        ll.append('CL')
    if 'g' in ll and 'H' in ll:
        ll.remove('g')
        ll.append('Hg')
    if '/' in ll:
        ll.remove('/')
    sorted_ll=['C','H','N','O','S']+list(set(ll)-{'C','H','N','O','S'})
    return sorted_ll

def get_molec_ind(molecule,formula):
    molec_count=formula.count(molecule)
    molec_ind=[]
    if molec_count==0:
        molec_ind.append(-1)
    
    if molec_count==1:
        if len(molecule)==1:
            molec_ind.append(formula.find(molecule))
        if len(molecule)==2:
            molec_ind.append(formula.find(molecule)+1)
    
    if molec_count>1:
        if len(molecule)==1:
            molec_ind.append(formula.find(molecule))
        if len(molecule)==2:
            molec_ind.append(formula.find(molecule)+1)
        
        new_f=formula[:molec_ind[0]]+'!'+formula[molec_ind[0]+1:]
        next_ind=new_f.find(molecule)
        molec_ind.append(next_ind)
        
        while next_ind!=-1:
            new_f=new_f[:next_ind]+'!'+new_f[next_ind+1:]
            next_ind=new_f.find(molecule)
            if next_ind!=-1:
                molec_ind.append(next_ind)
    return molec_ind
            

def get_nMolecule(molecule,formula):  
    molec_ind=get_molec_ind(molecule,formula)
    n=[]
    for iind in molec_ind:
        if iind!=-1:
            if formula[iind+1].isalpha():
                    n.append(1)
            if formula[iind+1].isdigit():
                if formula[iind+2].isdigit():
                    n.append(int(formula[iind+1]+formula[iind+2]))
                if formula[iind+2].isalpha():
                    n.append(int(formula[iind+1]))
        if iind==-1:
            n.append(np.nan)
    return pd.DataFrame(n).sum()[0]
    

def fix_seq_formula(formula,unique_molecule_list):    
    formula=formula+'Z'
    nCl=get_nMolecule('Cl',formula)
    nCL=get_nMolecule('CL',formula)
    nHg=get_nMolecule('Hg',formula)

    if nCl in [0,1]:
        formula=formula.replace('Cl','')
    else:
        formula=formula.replace('Cl'+str(int(nCl)),'')
    
    if nCL in [0,1]:
        formula=formula.replace('CL','')
    else:
        formula=formula.replace('CL'+str(int(nCL)),'')
    if nHg in [0,1]:
        formula=formula.replace('Hg','')
    else:
        formula=formula.replace('Hg'+str(int(nHg)),'')

    df=pd.DataFrame()
    df['Molecule']=unique_molecule_list
    df.loc[8,'nMolec']=nCL
    df.loc[10,'nMolec']=nCl
    df.loc[9,'nMolec']=nHg
    
    for i in df[~df['Molecule'].isin(['CL','Cl','Hg'])].index:
        df.loc[i,'nMolec']=get_nMolecule(df['Molecule'][i],formula)
    
    for i in df[df['nMolec']==0].index:
        df.loc[i,'package']=''
    
    for i in df[df['nMolec']==1].index:
        df.loc[i,'package']=df['Molecule'][i]
    
    for i in df[~df['nMolec'].isin([0,1])].index:
        df.loc[i,'package']=df['Molecule'][i]+str(int(df['nMolec'][i]))
                
    return ''.join(list(df['package']))
                
def OrderFormula(data):
    unique_molecule_list=['C', 'H', 'N', 'O', 'S', 'F', 'Br', 'I', 'CL', 'Hg', 'Cl']
    if 'formula' in data.columns:
        df=pd.DataFrame()
        data2=data[data['formula'].notna()]
        data2=data2[data2['pollutant category'].isin(['inorganic gas','NMOG'])]
        iind=list(data2.index)
        if len(iind)>0:
            for ind in iind:
                df.loc[ind,'formula']=(data['formula'].iloc[ind])
                ff=fix_seq_formula(data['formula'].iloc[ind],unique_molecule_list)
                if ff=='H3N':
                    ff='NH3'
                if ff=='CHN':
                    ff='HCN'
                if ff=='O2S':
                    ff='SO2'
                df.loc[ind,'formula(ordered)']=ff
                data.loc[ind,'formula']=ff
    if len(df)>0:
        df2=df[df['formula']!=df['formula(ordered)']]
        if len(df2)>0:
           col_list=['Formula','Formula(ordered)']
           t=create_PrettyTable_col2(col_list,list(df2['formula']),list(df2['formula(ordered)']))
           print('Formula column ordered-')
           print(t)
    return data




def nominal_mm_calulator(data):
    unique_molecule_list=['C', 'H', 'N', 'O', 'S', 'F', 'Br', 'I', 'CL', 'Hg', 'Cl']
    amass=[12,1,14,16,32,18,79,126,35,200,35]
    if 'formula' in data.columns:
        data2=data[data['formula'].notna()]
        data2=data2[data2['pollutant category'].isin(['inorganic gas','NMOG'])]
        iindex=list(data2.index)
        for i in iindex:
            formula=data['formula'].iloc[i]
            formula=formula+'A'
            fdf=pd.DataFrame()
            fdf['Molecule']=unique_molecule_list
            fdf['atmoc mass']=amass
            for k in range(len(fdf)):
                fdf.loc[k,'nMolecule']=get_nMolecule(fdf['Molecule'][k],formula)
            fdf['mass_nM']=fdf['atmoc mass']*fdf['nMolecule']
            data.loc[i,'mm']=fdf['mass_nM'].sum()
    # t=create_PrettyTable_col2(['formula','mass'],list(data['formula'][data.index.isin(iindex)]),list(data['mm'][data.index.isin(iindex)]))
    # print('Nominal mm calculated from formula column-')
    # print(t)
    return data


    
def exact_mm_calulator(data):
    unique_molecule_list=['C', 'H', 'N', 'O', 'S', 'F', 'Br', 'I', 'CL', 'Hg', 'Cl']
    amass=[12.0107,1.0078250319,14.003074004,15.9949146195,15.986035585,18.99840316,79.917315,126.904475,34.9688527,100.985322,34.9688527]
    
    if 'formula' in data.columns:
        data2=data[data['formula'].notna()]
        data2=data2[data2['pollutant category'].isin(['inorganic gas','NMOG'])]
        iindex=list(data2.index)
        for i in iindex:
            formula=data['formula'].iloc[i]
            formula=formula+'A'
            fdf=pd.DataFrame()
            fdf['Molecule']=unique_molecule_list
            fdf['atmoc mass']=amass
            for k in range(len(fdf)):
                fdf.loc[k,'nMolecule']=get_nMolecule(fdf['Molecule'][k],formula)
            fdf['mass_nM']=fdf['atmoc mass']*fdf['nMolecule']
            data.loc[i,'exact_mass']=fdf['mass_nM'].sum()
        t=create_PrettyTable_col2(['formula','mass'],list(data['formula'][data.index.isin(iindex)]),list(data['exact_mass'][data.index.isin(iindex)]))
        print(t)
    return data

    



















