# -*- coding: utf-8 -*-
"""
Created on Mon May 22 21:05:51 2023

@author: serve
"""

import pandas as pd
import os
import numpy as np
g = globals
path = r'C:\Users\serve\OneDrive\Desktop\TEA-Presentation\Data'
files = os.listdir(path)
ada = pd.read_csv(r'C:\Users\serve\OneDrive\Desktop\TEA-Presentation\ada.csv')
ada = ada[['District','District Name','  2016-2017 ADA ', '  2017-2018 ADA ', '  2018-2019 ADA ',
'  2019-2020 ADA ', '2020-2021 ADA', ' 2021-2022 ADA ']].rename(columns={'  2016-2017 ADA ':'ada17'
    , '  2017-2018 ADA ':'ada18' , '  2018-2019 ADA ':'ada19','  2019-2020 ADA ':'ada20'
    , '2020-2021 ADA':'ada21', ' 2021-2022 ADA ':'ada22'})
for col in ['ada17','ada18','ada19','ada20']:
    ada[col] = ada[col].str.replace(',','')
    ada[col] = ada[col].astype(float)
ada['District'] = ada['District'].astype(str).str.zfill(6)

for file in files:
    name = file[:-4]
    yr = name[-2:]
    g()[name] = pd.read_csv(path+'\\'+file)
    if name in ['enr19','enr20','enr21','enr22']:
        g()[name] = g()[name][['DISTRICT','ENROLLMENT']].rename(columns
                ={'DISTRICT':'District','ENROLLMENT':'enrollment'+yr})
        g()[name]['enrollment'+yr] = np.where(g()[name]['enrollment'+yr] == '<10',0
            , np.where(g()[name]['enrollment'+yr] == '<20', 10,np.where(g()[name]['enrollment'+yr] == '<50',40
                                                                        , g()[name]['enrollment'+yr])))
        g()[name]['enrollment'+yr] = g()[name]['enrollment'+yr].astype(float)
    else:
        g()[name] = g()[name][['District Number','Enrollment by Gender']].rename(columns
            ={'District Number':'District','Enrollment by Gender':'enrollment'+yr})

    g()[name] = g()[name].groupby('District').sum().reset_index()
    g()[name]['District'] = g()[name]['District'].astype(int)
    g()[name]['District'] = g()[name]['District'].astype(str).str.zfill(6)

df = ada.merge(enr17, on='District', how='left')\
    .merge(enr18, on='District', how='left')\
        .merge(enr19, on='District', how='left')\
            .merge(enr20, on='District', how='left')\
                .merge(enr21, on='District', how='left')\
                    .merge(enr22, on='District', how='left').fillna(0)
for yr in ['17','18','19','20','21','22']:
    df['ratio'+yr] = df['ada'+yr]/df['enrollment'+yr]

df.to_csv(path+'summary.csv')
