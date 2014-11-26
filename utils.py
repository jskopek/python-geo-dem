from osgeo import gdal
from osgeo import gdalconst
import struct
from datetime import datetime
import os
import sys


def altitude_at_raster_range(dataset, x1, y1, x2, y2):
    """
    Returns a two dimensional matrix of altitudes, in meters, for a range of two x/y raster points. 
    Requires a DEM dataset with corresponding data for the given x/y points
    """

    # the altitude data will be stored in raster band 1
    dem_band = dataset.GetRasterBand(1)

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

def altitude_at_raster_point(dataset, x, y):
    """
    Returns the altitude, in meters, for a given x/y raster point. Requires a DEM dataset with 
    corresponding data for the given x/y point
    """

    values = altitude_at_raster_range(dataset, x, y, x, y)
    return values[0][0]

def altitude_at_geographic_range(dataset, lon1, lat1, lon2, lat2):
    """
    Returns a two dimensional matrix of altitudes, in meters, for a given longitude/latitude range. 
    Requires a DEM dataset with corresponding data for the given lon/lat values
    """

    x1, y1 = geographic_coordinates_to_raster_points(dataset, lon1, lat1)
    x2, y2 = geographic_coordinates_to_raster_points(dataset, lon2, lat2)
    return altitude_at_raster_range(x1, y1, x2, y2)

def altitude_at_geographic_coordinates(dataset, lon, lat):
    """
    Returns the altitude, in meters, for a given longitude/latitude coordinate. Requires a DEM dataset with 
    corresponding data for the given lon/lat
    """

    x, y = geographic_coordinates_to_raster_points(dataset, lon, lat)
    return altitude_at_raster_point(dataset, x, y)

def geographic_coordinates_to_raster_points(dataset, lon, lat):
    """
    Converts a set of lon/lat points to x/y points using affine transformation. Note that the conversion is tied to the
    particular dataset. A particular lon/lat value will result in a different x/y point accross different datasets
    """

    # affine transformation to convert x/y points into lat/lon points
    transform = dataset.GetGeoTransform()

    # invert transformation so we can convert lat/lon to x/y
    success, transform_inverse = gdal.InvGeoTransform(transform)

    # apply transformation
    x, y = gdal.ApplyGeoTransform(transform_inverse, lon, lat)

    return (x,y)

def get_dem(dem_paths, lon, lat):
    """
    Given a particular longitude and latitude, loops though a list of dem paths until it finds a
    file that contains data on that point

    TODO: there's got to be a better way of determining which DEM file contains lon/lat
    """

    for dem_path in dem_paths:
        dataset = gdal.Open(dem_path)
        x, y = geographic_coordinates_to_raster_points(dataset, lon, lat)

        try:
            altitude_at_raster_point(dataset, x, y)
        except struct.error:
            continue
        else:
            return dem_path

    return False


lat = 49.456412
lon = -123.186007

lat=50
lon=-122
dem_files='a10g,b10g,c10g,d10g,e10g,f10g,g10g,h10g,i10g,j10g,k10g,l10g,m10g,n10g,o10g,p10g'
dem_paths = [os.path.join('store', dem_file) for dem_file in dem_files.split(',')]
dem_path = get_dem(dem_paths, lon, lat)
print dem_path
dataset = gdal.Open(dem_path)
x, y = geographic_coordinates_to_raster_points(dataset, lon, lat)
print x, y
values = altitude_at_raster_point(dataset, x, y)
print values

