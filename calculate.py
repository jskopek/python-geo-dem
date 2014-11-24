from osgeo import gdal
from osgeo import gdalconst
import struct
from datetime import datetime
import os
import sys


def calculate(dataset, min_x, min_y, max_x, max_y):
    # the altitude data will be stored in raster band 1
    dem_band = dataset.GetRasterBand(1)

    scanline_width = max_x - min_x + 1
    scanline_data_format = "<" + ("h" * scanline_width)

    data = []
    for y in range(min_y, max_y + 1):
        scanline = dem_band.ReadRaster(min_x, y, scanline_width, 1, scanline_width, 1, gdalconst.GDT_Int16)
        values = struct.unpack(scanline_data_format, scanline)
        data.append(values)
    return data

def calculate_point_coordinates(dataset, min_lat, min_lon, max_lat, max_lon):
    # determine the min & max x & y coordinates on the dataset from the lat/lon values
    transform = dataset.GetGeoTransform()
    success, transform_inverse = gdal.InvGeoTransform(transform)

    x1, y1 = gdal.ApplyGeoTransform(transform_inverse, min_lon, min_lat)
    x2, y2 = gdal.ApplyGeoTransform(transform_inverse, max_lon, max_lat)

    min_x = int(min(x1, x2))
    max_x = int(max(x1, x2))
    min_y = int(min(y1, y2))
    max_y = int(max(y1, y2))

    return (min_x, min_y, max_x, max_y)


def calculate_with_all_dems(min_lat, min_lon, max_lat, max_lon):
    dem_files='a10g,b10g,c10g,d10g,e10g,f10g,g10g,h10g,i10g,j10g,k10g,l10g,m10g,n10g,o10g,p10g'
    for dem_file in dem_files.split(','):
        dem_path = os.path.join('store', dem_file)
        try:
            dataset = gdal.Open(dem_path)
            coordinates = calculate_point_coordinates(dataset, min_lat, min_lon, max_lat, max_lon)
            data = calculate(dataset, *coordinates)
        except struct.error:
            continue
        else:
            return data

# these are the min/max lon/lat coordinates of NZ
#min_lon = 165
#max_lon = 179
#min_lat = -48
#max_lat = -33
#
#min_lon = -133
#max_lon = -110
#min_lat = 51
#max_lat = 58.2
#
#min_lon = -128.8
#max_lon = -120
#min_lat = 48
#max_lat = 49.95
#
print calculate_with_all_dems(min_lat=48, min_lon=-128.8, max_lat=49.95, max_lon=-120)

