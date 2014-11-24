from osgeo import gdal
from osgeo import gdalconst
import struct
from datetime import datetime
import os
import sys


# these are the min/max lon/lat coordinates of NZ
min_lon = -128.8
max_lon = -120
min_lat = 48
max_lat = 49.95

#min_lon = 165
#max_lon = 179
#min_lat = -48
#max_lat = -33




def calculate(dem_path, start_coords, end_coords):
    min_lat = start_coords[0]
    min_lon = start_coords[1]
    max_lat = end_coords[0]
    max_lon = end_coords[1]

    # first, let's load up the DEM file
    dataset = gdal.Open(dem_path)
    dem_band = dataset.GetRasterBand(1)

    # determine the min & max x & y coordinates on the dataset from the lat/lon values
    transform = dataset.GetGeoTransform()
    success, transform_inverse = gdal.InvGeoTransform(transform)

    x1, y1 = gdal.ApplyGeoTransform(transform_inverse, min_lon, min_lat)
    x2, y2 = gdal.ApplyGeoTransform(transform_inverse, max_lon, max_lat)

    min_x = int(min(x1, x2))
    max_x = int(max(x1, x2))
    min_y = int(min(y1, y2))
    max_y = int(max(y1, y2))

    scanline_width = max_x - min_x + 1
    scanline_data_format = "<" + ("h" * scanline_width)

    data = []
    for y in range(min_y, max_y + 1):
        scanline = dem_band.ReadRaster(min_x, y, scanline_width, 1, scanline_width, 1, gdalconst.GDT_Int16)
        values = struct.unpack(scanline_data_format, scanline)
        data.append(values)
    return data

def calculate_with_all_dems(start_coords, end_coords):
    dem_files='a10g,b10g,c10g,d10g,e10g,f10g,g10g,h10g,i10g,j10g,k10g,l10g,m10g,n10g,o10g,p10g'
    for dem_file in dem_files.split(','):
        dem_path = os.path.join('store', dem_file)
        try:
            data = calculate(dem_path, start_coords, end_coords)
        except struct.error:
            continue
        else:
            return data

calculate_with_all_dems((min_lat, min_lon), (max_lat, max_lon))
