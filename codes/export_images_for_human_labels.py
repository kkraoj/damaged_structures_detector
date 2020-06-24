# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:11:57 2020

@author: kkrao
"""


import os
import pandas as pd
import numpy as np

np.random.seed(11)


image_dir = "D:/Krishna/projects/damaged_structures_detector/images_for_human_labelling"
data_dir = "D:/Krishna/projects/damaged_structures_detector/data"

labels = pd.read_csv(os.path.join(data_dir,"image_labels_dictionary.csv"))
image_names = os.listdir(image_dir)


image_names = list(np.random.choice(image_names,size = len(image_names),replace = False))
image_names.remove("1701.jpg")
image_names.remove("3387.jpg")
image_names = ["1701.jpg", "3387.jpg"]+image_names


for image_name in image_names:
    print("=image(\"https://raw.githubusercontent.com/kkraoj/damaged_structures_detector/master/images_for_human_labelling/%s\",4,224,224)"%image_name)
    
for image_name in image_names:
    label = labels.loc[labels["IMAGENAME"]==image_name,'LABELBINARY'].values[0]
    if label=="destroyed":
        print("yes")
    else:
        print("no")

for image_name in image_names:
    print(image_name)

print(len(image_names))
