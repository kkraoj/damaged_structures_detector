# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 19:49:21 2020

@author: kkrao
"""


import ee
from ee import batch
import numpy as np

## Initialize (a ee python thing)
ee.Initialize()

dins = ee.FeatureCollection("users/kkraoj/damagedstructures/carrdins")
image = ee.ImageCollection.fromImages([ee.Image("users/kkraoj/damagedstructures/carr_0"),\
                                       ee.Image("users/kkraoj/damagedstructures/carr_1"),\
                                       ee.Image("users/kkraoj/damagedstructures/carr_2"),\
                                       ee.Image("users/kkraoj/damagedstructures/carr_3"),\
                                        ]).mosaic().select(['b1','b2','b3']) 

geometry = ee.Geometry.Rectangle(-122.4984934716851, 40.53765199638353,  -122.38039044434134, 40.62695683104033)
# print(geometry.getInfo())

footprints = ee.FeatureCollection("users/kkraoj/damagedstructures/building_footprints_carr").filterBounds(geometry)
print("Total footprints %0d"%footprints.size().getInfo())

dins = dins.filterMetadata('DAMAGE','equals','Destroyed (>50%)')
print("Total damaged labels %0d"%dins.size().getInfo())

spatialFilter = ee.Filter.intersects(leftField= '.geo', rightField= '.geo',  maxError= 0.3);

saveAllJoin = ee.Join.saveAll(matchesKey= 'matched')

damaged_footprints = saveAllJoin.apply(footprints, dins, spatialFilter);
damaged_footprints_size = damaged_footprints.size().getInfo()

print("Damaged footprints %0d"%damaged_footprints_size) ## 634 destroyed buildings. 

invertedJoin = ee.Join.inverted()

safe_footprints = invertedJoin.apply(footprints, damaged_footprints, spatialFilter);
safe_footprints_size = safe_footprints.size().getInfo()
print("Safe footprints %0d"%safe_footprints_size)

SCALE = 1e7


#%% damaged_export

# damaged_footprints_list = damaged_footprints.toList(damaged_footprints_size)

# for i in range(damaged_footprints_size):
#   print(i)
#   feature = ee.Feature(damaged_footprints_list.get(i))
#   region = feature.buffer(10).geometry().bounds()
#   # lon = ee.Number(feature.centroid().geometry().coordinates().get(0)).multiply(SCALE).round().getInfo()
#   # lat = ee.Number(feature.centroid().geometry().coordinates().get(1)).multiply(SCALE).round().getInfo()
#   name = "carr_%d"%(i)
  
#   task = ee.batch.Export.image.toDrive(
#   image= image,
#   folder='carr_safe_examples',
#   description= name,
#   scale= 0.1,
#   region= region
#   );
  
#   task.start()


#%%# safe_export


safe_footprints_list = safe_footprints.toList(safe_footprints_size)

random_samples = np.random.choice(range(safe_footprints_size),replace = False, size = 630*3)

ctr = 0
for i in random_samples:
  print(i)
   # print(type(i))
  feature = ee.Feature(safe_footprints_list.get(int(i)))
  region = feature.buffer(10).geometry().bounds()
  # lon = ee.Number(feature.centroid().geometry().coordinates().get(0)).multiply(SCALE).round().getInfo()
  # lat = ee.Number(feature.centroid().geometry().coordinates().get(1)).multiply(SCALE).round().getInfo()
  name = "carr_safe_%d"%ctr
  
  task = ee.batch.Export.image.toDrive(
  image= image,
  folder='carr_safe_really_examples',
  description= name,
  scale= 0.1,
  region= region ,
  dimensions = "165x165"
  );
  
  task.start()
  ctr+=1
# 3.1/1.2*64






