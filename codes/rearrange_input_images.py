# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:59:16 2020

@author: kkrao
"""

import shutil
import os
import pandas as pd
import numpy as np



dir_data = "D:/Krishna/projects/damaged_structures_detector/data"
dir_images = os.path.join(dir_data,'images')


np.random.seed(0)


#%% 
latlon = pd.read_csv(os.path.join(dir_data,"camp_fires_damage_assessment.csv"))
latlon = latlon.astype({'INDEX':int,'LATITUDE':float,'LONGITUDE':float,'DAMAGE':str})
latlon = latlon[['INDEX','LONGITUDE','LATITUDE','DAMAGE']]

latlon['IMAGENAME'] = latlon['INDEX'].astype(str)+".jpg"
latlon['LABELBINARY'] = "destroyed"

## whichever is not completely destroyed, label it as safe. 
latlon.loc[~(latlon.DAMAGE == 'Destroyed (>50%)'),'LABELBINARY'] = 'not_destroyed'
latlon['EXISTS'] = False
## remove the rows which donot have corresponding images because they were too close to the border. 
for file in os.listdir(dir_images):
    latlon.loc[latlon.IMAGENAME==file,'EXISTS'] = True

nlatlon = latlon.drop(latlon.loc[latlon['EXISTS']==False].index, axis =0)

nlatlon.to_csv(os.path.join(dir_data,'image_labels_dictionary.csv'))
nlatlon.drop('EXISTS',axis = 1,inplace = True)
latlon = nlatlon.copy()
nlatlon = None
#%%
TRAINRATIO = 0.85
VALRATIO= 0.1
TESTRATIO = 0.05 #600 images

total_images = latlon.shape[0]
test_inds = list(np.random.choice(latlon.loc[latlon.LABELBINARY=='not_destroyed'].index,size = 300,replace = False))
test_inds+=list(np.random.choice(latlon.loc[latlon.LABELBINARY=='destroyed'].index,size = 300,replace = False))
len(test_inds)
latlon['SET'] = 'train'
latlon.loc[test_inds,'SET'] = 'test'
# latlon.head()

###validation set


choose = int(VALRATIO*total_images*len(latlon.loc[(latlon.LABELBINARY=='not_destroyed')&(latlon.SET != 'test')])/len(latlon.loc[(latlon.LABELBINARY=='destroyed')&(latlon.SET != 'test')]))
inds = list(np.random.choice(latlon.loc[(latlon.LABELBINARY=='not_destroyed')&(latlon.SET != 'test')].index,size = choose,replace = False))
choose = int(VALRATIO*total_images - choose)
inds+=list(np.random.choice(latlon.loc[(latlon.LABELBINARY=='destroyed')&(latlon.SET != 'test')].index,size = choose,replace = False))

latlon.loc[inds,'SET'] = 'val'


#%% transfer images

for index, row in latlon.iterrows(): 
    old_path = os.path.join(dir_images,row.IMAGENAME)
    new_path = os.path.join(dir_images,row.SET,row.LABELBINARY,row.IMAGENAME)
    os.rename(old_path,new_path)