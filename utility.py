
# Battery Packages
import csv
import os
import os.path as osp

from glob import iglob as glob # iglob is a generator

import json

with open('resource.json') as fd:
    LOCATION = json.loads(fd.read())['storage_path']
    



def window(iterable, size):
    it  = iter(iterable)
    ret = [next(it) for _ in range(size)]

    yield ret
    for elm in it:
        ret = ret[1:] + [elm]
        yield ret



import sys
def uprint(*args, **kwargs):
    print(sys.path[0], *args, **kwargs)


def _path_resource(*paths):
    return osp.join(LOCATION, *paths)


def make_resource(*paths):
    """
    INPUT : comma seperated directories from local resource, followed by filename
    OUTPUT: full path of resource

    no errors thrown if resource already exists
    """
    *dirs, filename = paths
    dpath = _path_resource(*dirs)
    os.makedirs(dpath, exist_ok=True)
    fpath = osp.join(dpath, filename)
    return fpath

