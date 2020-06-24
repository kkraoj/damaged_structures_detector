# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:07:20 2020

@author: kkrao
"""


import os 
from PIL import Image, ImageOps
import numpy as np
import json
import matplotlib.pyplot as plt


dir_data = "D:/Krishna/projects/damaged_structures_detector/data/xbd"


# with open(os.path.join(dir_data, "train","labels","guatemala-volcano_00000000_post_disaster.json")) as f:
#   data = json.load(f)

#%%
# def assemble_stats():
# for folder in ["train","test","tier3","hold"]:
#     damage = []
#     for imagename in os.listdir(os.path.join(dir_data, folder,"labels")):
#         if ('fire' in imagename)&("post_disaster" in imagename):
#             with open(os.path.join(dir_data, folder,"labels",imagename)) as f:
#                 data = json.load(f)
#             for building in data['features']['xy']:
#                 damage.append(building['properties']['subtype'])
#     print("[INFO]\tPost Fire\tFolder: %s\tDestroyed Buildings:%d\tSafe Buildings:%d"%(folder, damage.count("destroyed"), damage.count("no-damage")))


#%% crop
EXTENDCROP = 1.2
DARK_THRESH = 2

def obtain_minmax(wkt):
    numbers = wkt.split('((')[1]
    numbers = numbers.split('))')[0]
    numbers = numbers.replace(',','')
    numbers = np.fromstring(numbers, float, sep = ' ')    
    xs = numbers[np.arange(0,len(numbers),2)]    
    ys = numbers[np.arange(1,len(numbers),2)] 
    
    return xs.min(), xs.max(), xs.mean(), ys.min(), ys.max(), ys.mean()    

# mctr = 0

def crop_images():
    heights = []
    mctr = 0
    for folder in ["train","test","tier3","hold"]:
        for imagename in os.listdir(os.path.join(dir_data, folder,"images")):
            if ('fire' in imagename)&("post_disaster" in imagename):
                arr = np.array(Image.open(os.path.join(dir_data, folder,"images",imagename))).astype(np.uint8)
                jsonname = imagename.split('.')[0]+'.json'
                with open(os.path.join(dir_data, folder,"labels",jsonname)) as f:
                    data = json.load(f)
                ctr=0
                for building in data['features']['xy']:
                    damage = building['properties']['subtype']
                    if (damage=='destroyed')|(damage=='no-damage'):
                        xmin, xmax, xc, ymin, ymax, yc= obtain_minmax(building['wkt'])
                        height = int(max((xmax - xmin),(ymax - ymin))*EXTENDCROP)
                        if (height>=32)&(height<=200):
                            left, top = int(xc - height/2), int(yc - height/2)
                            try:
                                shard = arr[top:top+height,left:left+height, :]
                                # print(shard.shape)
                                if np.mean(shard)>=DARK_THRESH:
                                    im = Image.fromarray(shard)
                                    savedamagefolder = 'a_not_destroyed'
                                    if damage=='destroyed':
                                        savedamagefolder = 'b_destroyed'    
                                    savename = os.path.join(dir_data, "crop",folder, savedamagefolder,imagename.split('.')[0]+'_%d'%ctr+'.jpg')
                                    im.save(savename)
                                    ctr+=1
                                    print("[INFO] Saving image %d"%mctr)
                                    mctr+=1
                                    heights.append(height)
                                    # return 1
                            except IndexError:
                                print('[INFO] Shard at border of mosaic. Skipping.')
    # plt.hist(heights)
    return heights
# heights = crop_images()

# fig, ax = plt.subplots(figsize = (3,3))
# ax.hist(heights, bins = 100)
# ax.set_xlim(0,200)
#%% augment

def augment_images(rotate_angle = 90):
    for folder in ["train","val"]:    
        subdir = os.path.join(dir_data, "crop",folder,"b_destroyed")
        filenames = os.listdir(subdir)
    # print(len(filenames))
        for filename in filenames:
          # if '_' not in filename:
            # image = utils.load_image_and_preprocess()
            angle = rotate_angle
            print(filename)
            while angle < 271:
                # print(angle)
                im = Image.open(os.path.join(subdir,filename))
                # arr = np.array(im)
                # plt.imshow(arr)
                # plt.show()
                im = im.rotate(angle)
                new_filename = os.path.splitext(filename)[0]+'_rotate_%s.jpg'%angle
                # print(new_filename)
                # im.save(os.path.join(directory,filename, "JPG")
                im.save(os.path.join(subdir,new_filename))
                # arr = np.array(im)
                # plt.imshow(arr)
                # plt.show()
                angle += rotate_angle
                # count += 1
            im = Image.open(os.path.join(subdir,filename))
            im = ImageOps.flip(im)
            new_filename = os.path.splitext(filename)[0]+'_flip.jpg'
            im.save(os.path.join(subdir,new_filename))
            # print(os.path.join(directory,new_filename))
            im = Image.open(os.path.join(subdir,filename))
            im = ImageOps.mirror(im)
            new_filename = os.path.splitext(filename)[0]+'_mirror.jpg'
            im.save(os.path.join(subdir,new_filename))


augment_images()
