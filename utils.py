from osgeo import gdal
from osgeo import gdalconst
import struct
from datetime import datetime
import os
import sys


def altitude_at_raster_range(x1, y1, x2, y2, dataset):
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

def altitude_at_raster_point(x, y, dataset):
    """
    Returns the altitude, in meters, for a given x/y raster point. Requires a DEM dataset with 
    corresponding data for the given x/y point
    """

    values = altitude_at_raster_range(x, y, x, y, dataset)
    return values[0][0]

def altitude_at_geographic_range(lon1, lat1, lon2, lat2, dataset=None):
    """
    Returns a two dimensional matrix of altitudes, in meters, for a given longitude/latitude range. 
    Requires a DEM dataset with corresponding data for the given lon/lat values
    """

    # load a dataset if one is not provided
    if not dataset:
        dataset = load_dataset(lon1, lat1)

    x1, y1 = geographic_coordinates_to_raster_points(lon1, lat1, dataset)
    x2, y2 = geographic_coordinates_to_raster_points(lon2, lat2, dataset)
    return altitude_at_raster_range(x1, y1, x2, y2, dataset)

def altitude_at_geographic_coordinates(lon, lat, dataset=None):
    """
    Returns the altitude, in meters, for a given longitude/latitude coordinate. Requires a DEM dataset with 
    corresponding data for the given lon/lat
    """

    # load a dataset if one is not provided
    if not dataset:
        dataset = load_dataset(lon, lat)

    x, y = geographic_coordinates_to_raster_points(lon, lat, dataset)
    return altitude_at_raster_point(x, y, dataset)

def geographic_coordinates_to_raster_points(lon, lat, dataset=None):
    """
    Converts a set of lon/lat points to x/y points using affine transformation. Note that the conversion is tied to the
    particular dataset. A particular lon/lat value will result in a different x/y point accross different datasets
    """

    # load a dataset if one is not provided
    if not dataset:
        dataset = load_dataset(lon, lat)

    # affine transformation to convert x/y points into lat/lon points
    transform = dataset.GetGeoTransform()

    # invert transformation so we can convert lat/lon to x/y
    success, transform_inverse = gdal.InvGeoTransform(transform)

    # apply transformation
    x, y = gdal.ApplyGeoTransform(transform_inverse, lon, lat)

    return (x,y)

def get_dem(lon, lat, dem_paths=None):
    """
    Given a particular longitude and latitude, loops though a list of dem paths until it finds a
    file that contains data on that point

    TODO: there's got to be a better way of determining which DEM file contains lon/lat
    """

    if not dem_paths:
        dem_paths = default_dem_paths()

    for dem_path in dem_paths:
        dataset = gdal.Open(dem_path)
        x, y = geographic_coordinates_to_raster_points(lon, lat, dataset)

        try:
            altitude_at_raster_point(x, y, dataset)
        except struct.error:
            continue
        else:
            return dem_path

    return False

def load_dataset(lon, lat, dem_paths=None):
    """
    Simple convenience method to wrap the initialization of a dem file into a dataset
    """

    dem_path = get_dem(lon, lat, dem_paths)
    return gdal.Open(dem_path)

def default_dem_paths():
    """
    Assuming a default `download_data.py` command was run, method generates a list of paths
    for where the extracted data should have gone
    """

    dem_files='a10g,b10g,c10g,d10g,e10g,f10g,g10g,h10g,i10g,j10g,k10g,l10g,m10g,n10g,o10g,p10g'
    dem_paths = [os.path.join('store', dem_file) for dem_file in dem_files.split(',')]
    return dem_paths
