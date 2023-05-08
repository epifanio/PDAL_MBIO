import glob
from string import Template
import pandas as pd
import pdal
import sys


def gen_input(directory, 
              file_extension='.ALL', 
              reader_driver='mbio', 
              file_format='MBF_EMOLDRAW', 
              output_type='pandas.DataFrame',
              reproject=False,
              in_srs=None,
              out_srs=None,
              verbose=False):
    assert output_type in ['numpy.array', 'pandas.DataFrame'], "Wrong output type"
    dirlist = "{directory}/*{file_extension}".format(directory=directory, 
                                                     file_extension=file_extension)

    file_list = glob.glob(dirlist)
    for result in file_list:
        if reproject and in_srs and out_srs:
            yield {"file_name": result, 
                   "reader_driver": reader_driver, 
                   "file_format": file_format, 
                   "output_type": output_type, 
                   "verbose": verbose,
                   "reproject": reproject,
                   "in_srs": in_srs,
                   "out_srs": out_srs}
        else:
            yield {"file_name": result, 
                   "reader_driver": reader_driver, 
                   "file_format": file_format, 
                   "output_type": output_type, 
                   "verbose": verbose}


def readEM1000_1(args):
    file_name = args['file_name'] 
    if 'reader_driver' in args:
        reader_driver = args['reader_driver']
    else:
        reader_driver = 'mbio'
    if 'file_format' in args:
        file_format = args['file_format']
    else:
        file_format = 'MBF_EMOLDRAW'
    if 'output_type' in args:
        output_type = args['output_type']
    else:
        output_type = 'numpy.array'
    assert output_type in ['numpy.array', 'pandas.DataFrame'], "rong output type"
    if 'verbose' in args:
        verbose = args['verbose']
    else:
        verbose = False
    t = Template('{"pipeline":[{"filename": "${file_name}","type":"readers.${reader_driver}","format" : "${file_format}"}]}')
    json = t.substitute(file_name=file_name, reader_driver=reader_driver, file_format = file_format)
    p = pdal.Pipeline(json)
    # p.validate()  # check if our JSON and options were good
    p.loglevel = 8  # really noisy
    count = p.execute()
    data = p.arrays[0]
    if verbose:
        if verbose == 1:
            print('Read', count, 'points with', len(data.dtype), 'dimensions')
        if verbose == 2:
            print('Read', count, 'points with', len(data.dtype), 'dimensions')
            print('Dimension names are', data.dtype.names)
        if verbose == 3:
            print('Read', count, 'points with', len(data.dtype), 'dimensions')
            print('Dimension names are', data.dtype.names)
            print('Metadata: ', p.metadata)
            print('Log: ', p.log)
    if output_type == 'numpy.array':
        return data
    if output_type == 'pandas.DataFrame':
        return pd.DataFrame(data)
    if output_type == 'count':
        return count


def read_mbraw2(args):
    file_name = args['file_name']
    if 'reader_driver' in args:
        reader_driver = args['reader_driver']
    else:
        reader_driver = 'mbio'
    if 'file_format' in args:
        file_format = args['file_format']
    else:
        file_format = 'MBF_EMOLDRAW'
    if 'output_type' in args:
        output_type = args['output_type']
    else:
        output_type = 'numpy.array'
    assert output_type in ['numpy.array', 'pandas.DataFrame'], "wrong output type"
    if 'verbose' in args:
        verbose = args['verbose']
    else:
        verbose = False
    if all(opt in args for opt in ['reproject', 'in_srs', 'out_srs']):
        # if args['reproject']:
        in_srs = args['in_srs']
        out_srs = args['out_srs']
        t = Template('{"pipeline":[{"filename": "${file_name}", "type":"readers.${reader_driver}","format" : "${file_format}"}, {"type":"filters.reprojection", "in_srs":"${in_srs}", "out_srs":"${out_srs}"}]}')
        json = t.substitute(file_name=file_name, 
                            reader_driver=reader_driver, 
                            file_format=file_format, 
                            in_srs=in_srs, 
                            out_srs=out_srs)

    else:
        t = Template('{"pipeline":[{"filename": "${file_name}","type":"readers.${reader_driver}","format" : "${file_format}"}]}')
        json = t.substitute(file_name=file_name, reader_driver=reader_driver, file_format = file_format) 
    # print(json)
    p = pdal.Pipeline(json)
    # p.validate()  # check if our JSON and options were good
    # p.loglevel = 8  # really noisy
    count = p.execute()
    data = p.arrays[0]
    if verbose:
        if verbose == 1:
            print('Read', count, 'points with', len(data.dtype), 'dimensions')
        if verbose == 2:
            print('Read', count, 'points with', len(data.dtype), 'dimensions')
            print('Dimension names are', data.dtype.names)
        if verbose == 3:
            print('Read', count, 'points with', len(data.dtype), 'dimensions')
            print('Dimension names are', data.dtype.names)
            print('Metadata: ', p.metadata)
            print('Log: ', p.log)
    if output_type == 'numpy.array':
        return data
    if output_type == 'pandas.DataFrame':
        return pd.DataFrame(data)
    if output_type == 'count':
        return count
    
def read_mbraw(args):
    file_name = args['file_name']
    if 'reader_driver' in args:
        reader_driver = args['reader_driver']
    else:
        reader_driver = 'mbio'
    if 'file_format' in args:
        file_format = args['file_format']
    else:
        file_format = 'MBF_EMOLDRAW'
        
        
    if 'output_type' in args:
        output_type = args['output_type']
    else:
        output_type = 'numpy.array'
    assert output_type in ['numpy.array', 'pandas.DataFrame'], "wrong output type"
    
    
    if all(opt in args for opt in ['reproject', 'in_srs', 'out_srs']):
        # if args['reproject']:
        in_srs = args['in_srs']
        out_srs = args['out_srs']
        t = Template('{"pipeline":[{"filename": "${file_name}", "type":"readers.${reader_driver}","format" : "${file_format}"}, {"type":"filters.reprojection", "in_srs":"${in_srs}", "out_srs":"${out_srs}"}]}')
        json = t.substitute(file_name=file_name, 
                            reader_driver=reader_driver, 
                            file_format=file_format, 
                            in_srs=in_srs, 
                            out_srs=out_srs)

    else:
        t = Template('{"pipeline":[{"filename": "${file_name}","type":"readers.${reader_driver}","format" : "${file_format}"}]}')
        json = t.substitute(file_name=file_name, reader_driver=reader_driver, file_format = file_format) 
    p = pdal.Pipeline(json)
    count = p.execute()
    data = p.arrays[0]

    if output_type == 'numpy.array':
        return data
    if output_type == 'pandas.DataFrame':
        return pd.DataFrame(data)
