# -*- coding: utf-8 -*-
"""
Created on Wed May 13 01:05:28 2020

@author: kkrao
"""

import gdal
import os
import pandas as pd
import numpy as np 
from PIL import Image



dir_data = "D:/Krishna/projects/damaged_structures_detector/data"


#%% damaged points
latlon = pd.read_csv(os.path.join(dir_data,"camp_fires_damage_assessment.csv"))
latlon = latlon[['INDEX','LONGITUDE','LATITUDE','DAMAGE']]
latlon = latlon.astype({'INDEX':int,'LATITUDE':float,'LONGITUDE':float,'DAMAGE':str})
latlon.head()

#%% input image
image = gdal.Open(os.path.join(dir_data,'paradise_aerial_image_projected.tif'))
# image = None
geotransform = image.GetGeoTransform()

def world_to_pixel(geo_matrix, lon, lat):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ul_x= geo_matrix[0]
    ul_y = geo_matrix[3]
    x_dist = geo_matrix[1]
    y_dist = geo_matrix[5]
    x = ((lon - ul_x) / x_dist).astype(int)
    y = -((ul_y - lat) / y_dist).astype(int)
    return x, y


latlon['X'], latlon['Y'] = world_to_pixel(geotransform, latlon.LONGITUDE, latlon.LATITUDE)


#%% create input images

dir_images = os.path.join(dir_data,'images')
height = 64 #same as width
DARK_THRESH = 2

arr = np.array(image.ReadAsArray()).astype(np.uint8)


for index, row in latlon.iterrows(): 
    
    left, top = int(row.X-height/2),int(row.Y-height/2)
    try:
        shard = arr[:,top:top+height,left:left+height]
        shard = np.moveaxis(shard, 0, -1)
        #check if shard is not in black (non imaged) zone
        if np.mean(shard)>=DARK_THRESH:
            im = Image.fromarray(shard)
            im.save(os.path.join(dir_images,'%d.jpg'%row.INDEX))
            print("[INFO] Saving image %d of %d"%(row.INDEX, latlon.shape[0]), flush=True)
        else:
            print('[INFO] Dark image encountered. Skipping.')
    except IndexError:
        print('[INFO] Shard at border of mosaic. Skipping.')
        continue