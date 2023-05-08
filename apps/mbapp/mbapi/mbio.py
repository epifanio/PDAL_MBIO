from fastapi.responses import RedirectResponse, FileResponse
from fastapi import Request, Query, APIRouter
from models.mbmodels import GeorefFile, mbformat_options, pdal_reader, pdal_ara, npmodel

from fastapi import FastAPI, File, UploadFile, Form, Depends
import pathlib
from fastapi.encoders import jsonable_encoder

from fastapi.responses import JSONResponse

from osgeo import gdal, osr
import shutil
import pathlib
import os
import subprocess
import tempfile
import json
from mbapi.mb_reader import gen_input, read_mbraw, readEM1000_1, read_mbraw2
from mbapi.mb_angle import run_it
from mbapi.mbformat import getFormats
import io
from pyarrow import csv
import numpy as np
router = APIRouter()

@router.get("/api/mbformat")
async def get_mbformat_list(form_data: mbformat_options = Depends()):
    return getFormats(form_data.format_name)


@router.post("/api/gdalinfo")
async def gdal_info(form_data: GeorefFile = Depends()):
    print(form_data.f)
    print('\n')
    # print(dir(form_data.f))
    print('\n')
    print(form_data.f.filename)
    print('\n')
    print(float(form_data.f.size) * 10E-06)
    # pathlib.Path('form_data.f.filename')
    print('\n')
    contents = await form_data.f.read()
    with open(f'/app/mbdata/{form_data.f.filename}', 'wb') as f:
        f.write(contents)
        f.flush()
    # rds = gdal.Open(form_data.f.filename)
    rds = gdal.Open(f'/app/mbdata/{form_data.f.filename}')
    metadata = rds.GetMetadata_Dict()
    metadata['size'] = float(form_data.f.size) * 10E-05
    gdalinfo_dict = {}
    gdalinfo_dict['filename'] = rds.GetDescription()
    gdalinfo_dict['projection'] = rds.GetProjection()
    gdalinfo_dict['geotransform'] = rds.GetGeoTransform()
    proj = osr.SpatialReference(wkt=gdalinfo_dict['projection'])
    proj.AutoIdentifyEPSG()
    gdalinfo_dict['EPSG'] = proj.GetAttrValue('AUTHORITY', 1)

    print('\n')
    print(rds.GetProjection())
    print('\n')
    print(rds.GetDescription())
    print('\n')
    print(rds.GetGeoTransform())
    print('\n')
    print(rds.GetMetadata_Dict())
    print('\n')
    # print(dir(rds.GetSpatialRef()))
    # print(type(rds.GetSpatialRef()))
    try:
        gdalinfo_dict['proj4'] = rds.GetSpatialRef().ExportToProj4()
        print(rds.GetSpatialRef().ExportToProj4())
    except AttributeError:
        print('No projection info found')
        print("NoneType' object has no attribute 'ExportToProj4")
        gdalinfo_dict['proj4'] = None
    gdalinfo_dict['metadata'] = metadata
    json_compatible_item_data = jsonable_encoder(gdalinfo_dict)
    return JSONResponse(content=json_compatible_item_data)

@router.post("/api/get_raw")
async def get_points(form_data: pdal_ara = Depends()):
    print(form_data)
    contents = await form_data.input_file.read()
    with open(f'/app/mbdata/{form_data.input_file.filename}', 'wb') as f:
        f.write(contents)
        f.flush()
    pdal_input = {"file_name": f'/app/mbdata/{form_data.input_file.filename}',
              "reader_driver": form_data.reader_driver, 
              "file_format": form_data.mb_formats.value, 
              "output_type": form_data.output_type.value, 
              "reproject": form_data.reproject,
              "in_srs": f"EPSG:{form_data.in_srs.value}",
              "out_srs": f"EPSG:{form_data.out_srs.value}",
              "verbose": form_data.verbose}
    data = read_mbraw(pdal_input)
    print(data)
    if form_data.output_type.value == 'numpy.array':
        if form_data.compute_angle:
            data = run_it(data)
            stream = io.BytesIO()
            csv.write_csv(data, stream)
            results = {'status': 'SUCCESS', 'data': stream.getvalue()}
            json_compatible_item_data = jsonable_encoder(results)
            return JSONResponse(content=json_compatible_item_data)
        else:
            stream = io.BytesIO()
            np.savetxt(stream, data, delimiter=',') 
            #results = {'status': 'SUCCESS', 'data': data.tolist()}
            results = {'status': 'SUCCESS', 'data': stream.getvalue()}
            json_compatible_item_data = jsonable_encoder(results)
            return JSONResponse(content=json_compatible_item_data)
    if form_data.output_type.value == 'pandas.DataFrame':
        if form_data.compute_angle:
            results = {'status': 'FAILED', 'data': 'angle computation for pandas dataframe not yet implemented'}
            json_compatible_item_data = jsonable_encoder(results)
            return JSONResponse(content=json_compatible_item_data)
        else:
            stream = io.StringIO()
            data.to_csv(stream, sep=";")
            results = {'status': 'SUCCESS', 'data': json.dumps(stream.getvalue())}
            json_compatible_item_data = jsonable_encoder(results)
            return JSONResponse(content=json_compatible_item_data)

    
    