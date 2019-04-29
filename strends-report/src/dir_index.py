# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:24:37 2019
Script to index of a directory of files 
shamlessly adapted from:
https://thomassileo.name/blog/2013/12/12/tracking-changes-in-directories-with-python/
@author: jsaracen
"""

import os
from setup_paths import DATA_PATH


def compute_diff(dir_base, dir_cmp):
    data = {}
    data['deleted'] = list(set(dir_cmp['files']) - set(dir_base['files']))
    data['created'] = list(set(dir_base['files']) - set(dir_cmp['files']))
    data['updated'] = []
    data['deleted_dirs'] = list(set(dir_cmp['subdirs']) - set(dir_base['subdirs']))

    for f in set(dir_cmp['files']).intersection(set(dir_base['files'])):
        if dir_base['index'][f] != dir_cmp['index'][f]:
            data['updated'].append(f)

    return data


def compute_dir_index(path):
    """ Return a tuple containing:
    - list of files (relative to path)
    - lisf of subdirs (relative to path)
    - a dict: filepath => last 
    """
    files = []
    subdirs = []

    for root, dirs, filenames in os.walk(path):
        for subdir in dirs:
            subdirs.append(os.path.relpath(os.path.join(root, subdir), path))

        for f in filenames:
            files.append(os.path.relpath(os.path.join(root, f), path))
        
    index = {}
    for f in files:
        index[f] = os.path.getmtime(os.path.join(path, f))

    return dict(files=files, subdirs=subdirs, index=index)

path = DATA_PATH 

diff = compute_dir_index(path)
