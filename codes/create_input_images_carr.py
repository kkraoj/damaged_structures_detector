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

#%% input image
image = gdal.Open(os.path.join(dir_data,'from_andrew','carr','carr_full_projected.tif'))
# image = None
geotransform = image.GetGeoTransform()
# EPSG:4326
arr = np.array(image.ReadAsArray()).astype(np.uint8)[:3,:,:]

# output_raster = os.path.join(dir_data,'from_andrew','carr','carr_full_projected.tif')
# gdal.Warp(output_raster,image,dstSRS='EPSG:4326')



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



#%% points

building_type = "safe"
latlon = pd.read_csv(os.path.join(dir_data,"carr_%s_footprints_centroids.csv"%building_type))
latlon['.geo'] = [x.split('[')[1] for x in latlon['.geo']]
latlon['LONGITUDE'] = [x.split(',')[0] for x in latlon['.geo']]
latlon['.geo'] = [x.split(',')[1] for x in latlon['.geo']]
latlon['LATITUDE'] = [x.split(']')[0] for x in latlon['.geo']]


latlon = latlon[['LONGITUDE','LATITUDE']]
latlon = latlon.astype({'LATITUDE':float,'LONGITUDE':float})
latlon.head()
latlon['X'], latlon['Y'] = world_to_pixel(geotransform, latlon.LONGITUDE, latlon.LATITUDE)

print('Original shape of latlon:')
print(latlon.shape)

latlon = latlon.loc[(latlon['X']>=0)&(latlon['Y']>=0)&(latlon['X']<arr.shape[2])&(latlon['Y']<arr.shape[1])]
print('Subsetted shape of latlon:')
print(latlon.shape)

#%% create input images

dirImages = os.path.join(dir_data,'images','%s_carr'%building_type)
height = 128 #same as width
DARK_THRESH = 2
LIGHT_THRESH = 250
SCALE = 1e7

#%% create input images

for f in files:
    os.remove(f)

# print(arr.shape)

ctr=0
# for index, row in latlon.iterrows(): 
for index, row in latlon.sample(3*630, random_state = 0,axis = 0).iterrows(): 
    left, top = int(row.X-height/2),int(row.Y-height/2)
    try:
        shard = arr[:3,top:top+height,left:left+height]
        shard = np.moveaxis(shard, 0, -1)
        # print(shard.shape)
        #check if shard is not in black (non imaged) zone
        if shard.shape!=(height, height, 3):
            print("[INFO] Image not square. Skipping.")
            continue
        if (np.mean(shard)>=DARK_THRESH)&(np.mean(shard)<=LIGHT_THRESH):
            im = Image.fromarray(shard)
            imageName = '{lon:.0f}_{lat:.0f}.jpg'.format(lon=row.LONGITUDE*SCALE,lat = row.LATITUDE*SCALE)
            # print(imageName)
            # break
            im.save(os.path.join(dirImages,imageName))
            print("[INFO] Saving image:\t %d "%ctr, flush=True)
            ctr+=1
        else:
            print('[INFO] Dark or White image encountered. Skipping.')
    except IndexError:
        print('[INFO] Shard at border of mosaic. Skipping.')
        continue


