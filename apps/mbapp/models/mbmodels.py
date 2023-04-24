from pydantic import BaseModel, Field
from typing import Optional, List, Union
import pydantic
import pydantic_numpy.dtype as pnd
from pydantic_numpy import NDArray, NDArrayFp32
from fastapi import UploadFile, Form


class GeorefFile(BaseModel):
    f: UploadFile = Form(...)
