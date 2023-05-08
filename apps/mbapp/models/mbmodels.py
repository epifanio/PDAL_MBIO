from pydantic import BaseModel, Field
from typing import Optional, List, Union
import pydantic
import pydantic_numpy.dtype as pnd
from pydantic_numpy import NDArray, NDArrayFp32
from fastapi import UploadFile, Form
from enum import Enum

from mbapi.mbformat import getFormats

class GeorefFile(BaseModel):
    f: UploadFile = Form(...)


class npmodel(BaseModel):
    coors: NDArray[pnd.float32] = Field(default=[0.0, 0.0], description='')
       
    
class mbformat_options(BaseModel):
    format_name: Optional[bool] = Field(
            default=False, title="Get only the MB System format name")
    
    
class pdal_reader(BaseModel):
    mb_formats : Enum('mb_formats', dict([('MBF_SBSIOMRG', 'MBF_SBSIOMRG'),
                                          ('MBF_SBSIOCEN', 'MBF_SBSIOCEN'),
                                          ('MBF_SBSIOLSI', 'MBF_SBSIOLSI'),
                                          ('MBF_SBURICEN', 'MBF_SBURICEN'),
                                          ('MBF_SBURIVAX', 'MBF_SBURIVAX'),
                                          ('MBF_SBSIOSWB', 'MBF_SBSIOSWB'),
                                          ('MBF_SBIFREMR', 'MBF_SBIFREMR'),
                                          ('MBF_HSATLRAW', 'MBF_HSATLRAW'),
                                          ('MBF_HSLDEDMB', 'MBF_HSLDEDMB'),
                                          ('MBF_HSURICEN', 'MBF_HSURICEN'),
                                          ('MBF_HSLDEOIH', 'MBF_HSLDEOIH'),
                                          ('MBF_HSURIVAX', 'MBF_HSURIVAX'),
                                          ('MBF_HSUNKNWN', 'MBF_HSUNKNWN'),
                                          ('MBF_SB2000SB', 'MBF_SB2000SB'),
                                          ('MBF_SB2000SS', 'MBF_SB2000SS'),
                                          ('MBF_SB2100RW', 'MBF_SB2100RW'),
                                          ('MBF_SB2100B1', 'MBF_SB2100B1'),
                                          ('MBF_SB2100B2', 'MBF_SB2100B2'),
                                          ('MBF_EMOLDRAW', 'MBF_EMOLDRAW'),
                                          ('MBF_EM12IFRM', 'MBF_EM12IFRM'),
                                          ('MBF_EM12DARW', 'MBF_EM12DARW'),
                                          ('MBF_EM300RAW', 'MBF_EM300RAW'),
                                          ('MBF_EM300MBA', 'MBF_EM300MBA'),
                                          ('MBF_EM710RAW', 'MBF_EM710RAW'),
                                          ('MBF_EM710MBA', 'MBF_EM710MBA'),
                                          ('MBF_MR1PRHIG', 'MBF_MR1PRHIG'),
                                          ('MBF_MR1ALDEO', 'MBF_MR1ALDEO'),
                                          ('MBF_MR1BLDEO', 'MBF_MR1BLDEO'),
                                          ('MBF_MR1PRVR2', 'MBF_MR1PRVR2'),
                                          ('MBF_MBLDEOIH', 'MBF_MBLDEOIH'),
                                          ('MBF_MBNETCDF', 'MBF_MBNETCDF'),
                                          ('MBF_MBNCDFXT', 'MBF_MBNCDFXT'),
                                          ('MBF_CBAT9001', 'MBF_CBAT9001'),
                                          ('MBF_CBAT8101', 'MBF_CBAT8101'),
                                          ('MBF_HYPC8101', 'MBF_HYPC8101'),
                                          ('MBF_XTFR8101', 'MBF_XTFR8101'),
                                          ('MBF_RESON7KR', 'MBF_RESON7KR'),
                                          ('MBF_RESON7K3', 'MBF_RESON7K3'),
                                          ('MBF_BCHRTUNB', 'MBF_BCHRTUNB'),
                                          ('MBF_ELMK2UNB', 'MBF_ELMK2UNB'),
                                          ('MBF_BCHRXUNB', 'MBF_BCHRXUNB'),
                                          ('MBF_L3XSERAW', 'MBF_L3XSERAW'),
                                          ('MBF_HSMDARAW', 'MBF_HSMDARAW'),
                                          ('MBF_HSMDLDIH', 'MBF_HSMDLDIH'),
                                          ('MBF_DSL120PF', 'MBF_DSL120PF'),
                                          ('MBF_DSL120SF', 'MBF_DSL120SF'),
                                          ('MBF_GSFGENMB', 'MBF_GSFGENMB'),
                                          ('MBF_MSTIFFSS', 'MBF_MSTIFFSS'),
                                          ('MBF_EDGJSTAR', 'MBF_EDGJSTAR'),
                                          ('MBF_EDGJSTR2', 'MBF_EDGJSTR2'),
                                          ('MBF_OICGEODA', 'MBF_OICGEODA'),
                                          ('MBF_OICMBARI', 'MBF_OICMBARI'),
                                          ('MBF_OMGHDCSJ', 'MBF_OMGHDCSJ'),
                                          ('MBF_SEGYSEGY', 'MBF_SEGYSEGY'),
                                          ('MBF_MGD77DAT', 'MBF_MGD77DAT'),
                                          ('MBF_ASCIIXYZ', 'MBF_ASCIIXYZ'),
                                          ('MBF_ASCIIYXZ', 'MBF_ASCIIYXZ'),
                                          ('MBF_HYDROB93', 'MBF_HYDROB93'),
                                          ('MBF_MBARIROV', 'MBF_MBARIROV'),
                                          ('MBF_MBPRONAV', 'MBF_MBPRONAV'),
                                          ('MBF_NVNETCDF', 'MBF_NVNETCDF'),
                                          ('MBF_ASCIIXYT', 'MBF_ASCIIXYT'),
                                          ('MBF_ASCIIYXT', 'MBF_ASCIIYXT'),
                                          ('MBF_MBARROV2', 'MBF_MBARROV2'),
                                          ('MBF_HS10JAMS', 'MBF_HS10JAMS'),
                                          ('MBF_HIR2RNAV', 'MBF_HIR2RNAV'),
                                          ('MBF_MGD77TXT', 'MBF_MGD77TXT'),
                                          ('MBF_MGD77TAB', 'MBF_MGD77TAB'),
                                          ('MBF_SAMESURF', 'MBF_SAMESURF'),
                                          ('MBF_HSDS2RAW', 'MBF_HSDS2RAW'),
                                          ('MBF_HSDS2LAM', 'MBF_HSDS2LAM'),
                                          ('MBF_IMAGE83P', 'MBF_IMAGE83P'),
                                          ('MBF_IMAGEMBA', 'MBF_IMAGEMBA'),
                                          ('MBF_HYSWEEP1', 'MBF_HYSWEEP1'),
                                          ('MBF_XTFB1624', 'MBF_XTFB1624'),
                                          ('MBF_SWPLSSXI', 'MBF_SWPLSSXI'),
                                          ('MBF_SWPLSSXP', 'MBF_SWPLSSXP'),
                                          ('MBF_3DDEPTHP', 'MBF_3DDEPTHP'),
                                          ('MBF_3DWISSLR', 'MBF_3DWISSLR'),
                                          ('MBF_3DWISSLP', 'MBF_3DWISSLP'),
                                          ('MBF_WASSPENL', 'MBF_WASSPENL'),
                                          ('MBF_PHOTGRAM', 'MBF_PHOTGRAM'),
                                          ('MBF_KEMKMALL', 'MBF_KEMKMALL')])) = 'MBF_EMOLDRAW'
    input_file: UploadFile = Form(...) 
    reader_driver: str = Field(default='mbio')
    output_type : Enum('output_type', dict([('numpy.array', 'numpy.array'),('pandas.DataFrame','pandas.DataFrame') ])) = 'numpy.array'
    verbose: Optional[bool] = Field(
            default=False, title="Get only the MB System format name")
    
    
    
class pdal_ara(BaseModel):
    mb_formats : Enum('mb_formats', dict([(i,i) for i in getFormats(format_name=True)])) = 'MBF_EMOLDRAW'
    input_file: UploadFile = Form(...) 
    reader_driver: str = Field(default='mbio')
    output_type : Enum('output_type', dict([('numpy.array', 'numpy.array'),('pandas.DataFrame','pandas.DataFrame') ])) = 'numpy.array'
    reproject : Optional[bool] = Field(default=False, title="Reproject")
    in_srs : Enum('in_proj', dict([('4326', '4326'),('32619','32619'),('32618','32618') ])) = 4326
    out_srs : Enum('out_proj', dict([('4326', '4326'),('32619','32619'), ('32618','32618') ])) = 4326
    compute_angle : Optional[bool] = Field(
        default=False, title="Compute Angle")
    verbose: Optional[bool] = Field(
        default=False, title="Get only the MB System format name")