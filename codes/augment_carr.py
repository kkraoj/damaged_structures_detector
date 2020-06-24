# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 12:48:02 2020

@author: kkrao
"""

import os
import numpy as np 
from PIL import Image



dir_data = "D:/Krishna/projects/damaged_structures_detector/data"
building_type = "damaged"
dirImages = os.path.join(dir_data,'images','%s_carr'%building_type)




def augment_images(directory=None, rotate_angle = 90 ):
    filenames = os.listdir(directory)
    # print(len(filenames))
    for filename in filenames:
      # if '_' not in filename:
        # image = utils.load_image_and_preprocess()
        angle = rotate_angle
        print(filename)
        while angle < 181:
            # print(angle)
            im = Image.open(os.path.join(directory,filename))
            # arr = np.array(im)
            # plt.imshow(arr)
            # plt.show()
            im = im.rotate(angle)
            new_filename = os.path.splitext(filename)[0]+'_rotate_%s.jpg'%angle
            # print(new_filename)
            # im.save(os.path.join(directory,filename, "JPG")
            im.save(os.path.join(directory,new_filename))
            # arr = np.array(im)
            # plt.imshow(arr)
            # plt.show()
            angle += rotate_angle
            # count += 1
        # im = Image.open(os.path.join(directory,filename))
        # im = ImageOps.flip(im)
        # new_filename = os.path.splitext(filename)[0]+'_flip.jpg'
        # im.save(os.path.join(directory,new_filename))
        # print(os.path.join(directory,new_filename))
        # im = Image.open(os.path.join(directory,filename))
        # im = ImageOps.mirror(im)
        # new_filename = os.path.splitext(filename)[0]+'_mirror.jpg'
        # im.save(os.path.join(directory,new_filename))

augment_images(os.path.join(dirImages))
