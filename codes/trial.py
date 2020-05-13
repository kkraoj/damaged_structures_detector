# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:04:02 2020

@author: kkrao
"""
import geojson, gdal, subprocess


path_to_file = r"C:\Users\kkrao\Desktop\California.geojson"

with open(path_to_file) as f:
    gj = geojson.load(f)
features = gj['features'][0]


args = ['ogr2ogr', '-f', 'ESRI Shapefile',  r"C:\Users\kkrao\Desktop\California.shp", 'path_to_file']
subprocess.Popen(args)
