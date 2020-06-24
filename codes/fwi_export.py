# -*- coding: utf-8 -*-
"""
Created on Mon May 25 19:27:31 2020

@author: kkrao
"""

import numpy as np
import pandas as pd
import os
import time
import datetime
from pandas.tseries.offsets import DateOffset


df = pd.DataFrame({'id_no': os.listdir("D:\Krishna\projects\wildfire_from_lfmc\data\FWI\python_export")})
df['system:time_start'] = pd.to_datetime([x.split('.')[0][-10:] for x in df['id_no']],format = '%Y_%m_%d')

df['id_no'] = df['id_no'].str[:-4]
# df['system:time_start'].

files = os.listdir("D:\Krishna\projects\wildfire_from_lfmc\data\FWI\python_export")
startdates = [x.split('.')[0][-10:] for x in df['id_no']]
# enddates = pd.to_datetime(startdates) + DateOffset(days = -1)
# enddates = [x.strftime("%Y-%m-%d") for x in enddates]

# for file in files:
#     print(file[:-4])
# enddates.pop(0)
# enddates.append('2019-12-31')

# unixtimes = [time.mktime(datetime.datetime.strptime(s, "%Y_%m_%d").timetuple()) for s in startdates]
df['system:time_start'] = [time.mktime(datetime.datetime.strptime(s, "%Y_%m_%d").timetuple()) for s in startdates]
df['system:time_start']  = df['system:time_start'].astype(np.int64)*1000
df['system:time_end'] =df['system:time_start']+86400000-1

df.head()
df.index = df['id_no']
df.drop('id_no',axis = 1, inplace = True)

df.to_csv(os.path.join("D:/Krishna/projects/wildfire_from_lfmc/data/FWI",'upload_meta_data.csv'))


### ALWAYS USE geeup selsetup
###geeup upload -u kkrao.j@gmail.com --source "D:/Krishna/projects/wildfire_from_lfmc/data/FWI/python_export" --dest "users/kkraoj/wildfire/fwi_col" --metadata "D:/Krishna/projects/wildfire_from_lfmc/data/FWI/upload_meta_data.csv" --nodata -9999
#geeup upload -u kkrao.j@gmail.com --source "D:\Krishna\projects\wildfire_from_lfmc\data\FWI\python_export_trial" --dest "users/kkraoj/wildfire/fwi_col" --metadata "D:\Krishna\projects\wildfire_from_lfmc\data\FWI\upload_meta_data_trial.csv" --nodata -9999
