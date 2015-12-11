# -*- coding: utf-8 -*-

# Create a pair of image list file (train/val) for Caffe training
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

NUM_SKETCH=10000
NUM_VAL=10000
#paint_path='/home/ispick/Projects/images/single_characters_10000'
paint_path='/home/ispick/Projects/illust_detection/detect_natural_images/clipart-benchmark'
paint_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(paint_path) for f in filenames]
image_paths_paint = []
dir_path = os.getcwd()

print 'searching illustrations...'
print paint_files[0]
for idx, filepath in enumerate(paint_files):
    if not ' ' in filepath:
        image_paths_paint.append(filepath)
        #image_paths_paint.append(paint_path + '/' + filepath)
    if idx == NUM_SKETCH-1:
        break
    if idx % 1000 == 0:
        print idx
print len(image_paths_paint)


paint_ids = np.empty(len(image_paths_paint), dtype=int)
paint_ids.fill(1)
data_x = image_paths_paint
data_y = paint_ids.tolist()
data = zip(data_x, data_y)
shuffle(data)


# Split data to train/val
with open('test_clipart', 'w') as ft:#test_illust
    for idx, d in enumerate(data):
        ft.write('%s %d\n' % (d[0], d[1]))

