python-geo-dem
============================

A Python library that simplifies the process of obtaining altitude data for a set of lat/long points

Downloading Geographic Data
=============================

Before you begin using the geographic libraries, you must download the required altitude data files. The library is capable
of handling DEM altitude files obtained via GLOBE, a research project run by the NOAA. To download a global set of data, simply
run the command

`python download_data.py`

Note that the full GLOBE data will take approximately 1.8GB

Determining Altitude
=============================

Assuming a full set of data has been downloaded to the default directory via the `download_data.py` command, usage is very
straightforward.

To get the altitude (in meters) at a given longitude/latitude point:

    from geodem.utils import altitude_at_geographic_coordinates
    altitude = altitude_at_geographic_coordinates(lon=-122, 50)
    print altitude # => 951

To get the altitude for a given range

    from geodem.utils import altitude_at_geographic_coordinates
    altitudes = altitude_at_geographic_range(lon1=-122, lat1=50, lon2=-122 - 0.01, lat2=50 - 0.01)
    print altitudes # => [(938, 681, 951), (1163, 728, 727)]


 

Methods - Advanced Usage
=============================

`geodem.utils.get_dem(dem_paths, lon, lat)`

Given a particular longitude and latitude, loops though a list of dem paths until it finds a file that contains data for that point

Example:

    dem_files='a10g,b10g,c10g,d10g,e10g,f10g,g10g,h10g,i10g,j10g,k10g,l10g,m10g,n10g,o10g,p10g'
    dem_paths = [os.path.join('store', dem_file) for dem_file in dem_files.split(',')]
    dem_path = get_dem(dem_paths, lon=-122, lat=50) # => store/10g
  
`geodem.utils.load_dataset(dem_paths, lon, lat)`

Simple convenience method to wrap the initialization of a dem file into a dataset
