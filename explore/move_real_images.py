# -*- coding: utf-8 -*-

import os
import json
from matplotlib import pyplot
import numpy as np
from PIL import Image
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from random import shuffle
import shutil
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

real_path='real'
real_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(real_path) for f in filenames if os.path.splitext(f)[1] == '.jpg']

dist_path='bof_data/0'

for path in real_files:
	print path
	shutil.copyfile(path, dist_path+'/'+path_leaf(path))