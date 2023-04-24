from fastapi.responses import RedirectResponse, FileResponse
from fastapi import Request, Query, APIRouter
from models.mbmodels import GeorefFile

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

from mbapi.mb_reader import gen_input, readEM1000, readEM1000_1

router = APIRouter()


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