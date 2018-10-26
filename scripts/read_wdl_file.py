# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 16:32:43 2018
script to read in WDL query
@author: jsaracen
"""
import pandas as pd
filename = 'WDL_B9D74051159_C10.xls'
filename = 'all cache data to 2018.xlsx'
filename = 'test data.xlsx'

data = pd.read_excel(filename, skiprows=1, skipfooter=3,
                    index_col=[5], na_values=['nan','na',], )
data.replace('< R.L.', 0)
#if isinstance(data.index, pd.DatetimeIndex):
#    data.index= pd.to_datetime(data.index.round('15Min'))
