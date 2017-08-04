#!/usr/bin/env python

import os

def ensure_dir_path_exists(path):
    dir_path = os.path.dirname(path)
    if dir_path == '' or os.path.isdir(dir_path):
        return
    os.makedirs(dir_path)
