
# Battery Packages
import csv
import os
import os.path as osp

from glob import iglob as glob # iglob is a generator

# REMOTE RESOURCES
from appdirs import user_data_dir
LOCATION = '/media/terra/UndecidedTeam'

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
    os.utime(fpath, None)
    return fpath

