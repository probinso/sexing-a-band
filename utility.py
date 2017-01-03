
# Battery Packages
import csv
import os
import os.path as osp

from glob import iglob as glob # iglob is a generator

import json

with open('resource.json') as fd:
    LOCATION = json.loads(fd.read())['storage_path']
    

def getdict(filename):
    resource = make_resource(filename)
    with open(resource) as fd:
        it = iter(fd)
        dline = next(it)
        stri = lambda s: s.strip()
        return {word : key for key, word in enumerate(map(stri, dline[1:].split(',')), 1)}

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

