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
paint_path='wikipaintings'
real_path='real'
paint_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(paint_path) for f in filenames]
real_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(real_path) for f in filenames if os.path.splitext(f)[1] == '.jpg']
image_paths_sketch = []
image_paths_real = []
image_paths_paint = []

dir_path = os.getcwd()
print 'searching real images...'
for idx, filepath in enumerate(real_files[10000:]):
    image_paths_real.append(dir_path + '/' + filepath)
    #image_paths_real.append(filepath)
    if len(image_paths_real) == NUM_SKETCH-1:
        break
    if idx % 1000 == 0:
        print idx
print image_paths_real[0]


# check if the file is corrupt, and remove images if corrupted
print 'removing corrupted paintings...'
import cv2
print len(paint_files)
#cleaned_paint_files = [filepath for filepath in paint_files if not cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR) is None and not ' ' in filepath ]
cleaned_paint_paths=[]
for idx, filepath in enumerate(paint_files[10000:]):
    if not cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR) is None and not ' ' in filepath:
        cleaned_paint_paths.append(filepath)
    if idx % 1000 == 0:
        print idx
    if len(cleaned_paint_paths) == NUM_SKETCH-1:
        break
print len(cleaned_paint_paths)

print 'searching paintings...'
print paint_files[0]
for idx, filepath in enumerate(cleaned_paint_paths):
    #if not ' ' in filepath:
        #image_paths_paint.append(filepath)
    image_paths_paint.append(dir_path + '/' + filepath)
    if idx == NUM_SKETCH-1:
        break
    if idx % 1000 == 0:
        print idx


"""print 'searching sketches...'
for idx, filepath in enumerate(sketch_image):
    # Avoid space included dir names
    if ' ' in filepath:
        continue
    #image_paths_sketch.append('sketch/' + filepath)
    image_paths_sketch.append(dir_path + '/sketch/' + filepath)
    if idx == NUM_SKETCH-1:
        break
    if idx % 1000 == 0:
        print idx
print image_paths_sketch[0]"""

#sketch_ids = np.empty(len(image_paths_sketch), dtype=int)
#sketch_ids.fill(1)
paint_ids = np.empty(len(image_paths_paint), dtype=int)
paint_ids.fill(1)
real_ids = np.empty(len(image_paths_real), dtype=int)
real_ids.fill(0)

data_x = image_paths_real+image_paths_paint
data_y = real_ids.tolist()+paint_ids.tolist()
data = zip(data_x, data_y)
shuffle(data)


# Split data to train/val
with open('test', 'w') as ft:
    for idx, d in enumerate(data):
        ft.write('%s %d\n' % (d[0], d[1]))

