# PDAL_MBIO

A FastAPI app to access GRASS and Mb-System functionalities.

## The list of implemented modules includes:
**GRASS GIS**
* `gisenv`: get the GRASS session environment 
* `create_location_epsg`: create GRASS Location from EPSG code
*  `create_location_file`: create GRASS Location from georeferenced file
*  `create_mapset`: create GRASS Location Mapset for an existent GRASS Location
*  `set_region_bounds`: set GRASS Computatinal Region bounds (n,s,w,e)
*  `set_region_raster`: set GRASS Computatinal Region from a raster layer
*  `get_raster_list`: get a list of available raster Layer
*  `geomorphon`: run `r.geomorphon` on a given elevation layer and computational region
*  `paramscale`: run `r.param.scale` on a given elevation layer and computational region
*  `r_what`: run `r.what` on a given location on a list of raster layers
*  `m_proj`: conver coodinates using `m.proj`
*  `get_current_region`: get the current GRASS computational region
*  `g_remove`: run `g.remove` on active GRASS Location/Mapset
*  `clear_tmp`: clear `/tmp` directory
*  `get_location_list`: get a list of available GRASS Location
*  `get_rgv_list`: run `g.list` to retrieve a list of available saved region, raster and vector layers
*  `GRM`: run a GIS Rule Base Model (LSI)
**MB-System**
* `mbformat`: return a description for available driver
* `get_raw`: extraxt X,Y,Z from supported sonar data
  * `reproject`: optional, reproject the data to a given SRS (uses EPSG codes)
  * `compute_angle`: extract incidence angle for each beam
**GDAL**
* `gdalinfo`: upload a georeferences file and ruturn info from the `gdalinfo` command

Example request


```python
import requests

headers = {
    'accept': 'application/json',
}

params = {
    'format_name': 'true',
}

response = requests.get('https://mbapi/api/mbformat', params=params, headers=headers)
response.json()
```

Requirements

[Docker Setup](docker/README.md)

