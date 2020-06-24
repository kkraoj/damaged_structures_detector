#!/usr/bin/env python2
"""
Script that allows for conversion of a netcdf file to
a stack of geotiff files with each raster being a time
slice from the input file.

Base implementation taken from:
https://www.linkedin.com/pulse/convert-netcdf4-file-geotiff-using-python-chonghua-yin

Usage:
    ./nc_to_gtiff.py varname infile.nc outdir
"""

import os
import sys
from osgeo import gdal, osr, gdal_array
import xarray as xr
import numpy as np
import pandas as pd


def get_netcdf_info(fname, var):
    print('Creating GDAL datastructures')
    subset = 'NETCDF:"' + fname + '":' + var
    sub_ds = gdal.Open(subset)
    nodata = sub_ds.GetRasterBand(1).GetNoDataValue()
    xsize = sub_ds.RasterXSize
    ysize = sub_ds.RasterYSize
    geot = sub_ds.GetGeoTransform()
    proj = osr.SpatialReference()
    # proj.SetWellKnownGeogCS('NAD27')
    return nodata, xsize, ysize, geot, proj


def create_geotiff(suffix, data, ndv, xsize, ysize, geot, proj):
    dt = gdal_array.NumericTypeCodeToGDALTypeCode(data[BAND_VARS[0]].values.dtype)
    if type(dt) != np.int:
        if dt.startswith('gdal.GDT_') is False:
            dt = eval('gdal.GDT_'+dt)
    new_fname = suffix + '.tif'
    zsize = len(BAND_VARS)
    driver = gdal.GetDriverByName('GTiff')
    ds = driver.Create(new_fname, xsize, ysize, zsize, dt)
    ds.SetProjection(proj.ExportToWkt())
    ds.SetGeoTransform(geot)
    for i, var in enumerate(BAND_VARS):
        # d = np.flip(data[var].values, 0)
        d = data[var].values
        d[np.isnan(d)] = ndv
        ds.GetRasterBand(i+1).WriteArray(d)
        ds.GetRasterBand(i+1).SetNoDataValue(ndv)
    ds.FlushCache()
    return new_fname

def calculate_band_stats(fname, var):
    print('Calculating band stats')
    ds = xr.open_dataset(fname,decode_times = False)
    results = []
    ds = ds[var]
    print('  Calculating mean')
    ds_weekly = ds.resample(time='1M').mean().to_dataset().rename({var: 'mean'})
    # print('  Calculating min')
    # ds_weekly['min'] = ds.resample('1M', dim='time', how='min')
    # print('  Calculating max')
    # ds_weekly['max'] = ds.resample('1M', dim='time', how='max')
    # print('  Calculating std')
    # ds_weekly['std'] = ds.resample('1M', dim='time', how='std')
    # print('  Calculating median')
    # ds_weekly['median'] = ds.resample('1M', dim='time', how='median')
    return ds_weekly


BAND_VARS = ['fwi']

def main(args):
	varname, infile, outdir, outname = args
	if os.path.exists(outdir) and os.path.isfile(outdir):
		exit("Output path exists and is a regular file! \n"
	    	 "Please provide a new output directory and try again")
	if not os.path.exists(outdir):
		os.mkdir(outdir)
    ## manually assigned arguments and ran from here onwards below. 
    for year in range(2016,2020):
        infile_short = "westFWI_%04d.nc"%year
        infile = os.path.join("D:/Krishna/projects/wildfire_from_lfmc/data/FWI",infile_short)
        data = xr.open_dataset(infile,decode_times = False)
        ndv, xs, ys, geot, proj = get_netcdf_info(infile, varname)
        
        #data = calculate_ban_stats(infile, varname)
        dates = data.time.values
        n_bands = len(BAND_VARS)
        n_iter = len(dates)
        for i in range(n_iter):
            date = pd.to_datetime('%04d-%03d'%(year, i+1),format = '%Y-%j').strftime('%Y_%m_%d')
            print(date)
            create_geotiff('{}{}out_{}_{}'.format(outdir, os.path.sep, outname, date),\
            data.isel(time=i), ndv, xs, ys, geot, proj)
        # break