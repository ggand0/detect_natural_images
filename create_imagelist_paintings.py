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

IMAGE_PER_CLASS=5
NUM_SKETCH=10000
IMG_SIZE=256#64
NUM_VAL=10000
sketch_path='sketch'
paint_path='wikipaintings'
real_path='real'
#sketch_files = [ f for f in listdir(sketch_path) if isfile(join(sketch_path,f)) ]

#paint_files = [ f for f in listdir(paint_path) if isfile(join(paint_path,f)) ]
paint_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(paint_path) for f in filenames]
real_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(real_path) for f in filenames if os.path.splitext(f)[1] == '.jpg']
sketch_dirs = [x[0] for x in os.walk(sketch_path)]
sketch_images=[]
with open('sketch/filelist.txt') as f:
    sketch_image = f.read().splitlines()
image_paths_sketch = []
image_paths_real = []
image_paths_paint = []


dir_path = os.getcwd()
print 'searching real images...'
for idx, filepath in enumerate(real_files):
    image_paths_real.append(dir_path + '/' + filepath)
    #image_paths_real.append(filepath)
    if idx == NUM_SKETCH-1:
        break
    if idx % 1000 == 0:
        print idx
print image_paths_real[0]


print 'searching paintings...'
print paint_files[0]
for idx, filepath in enumerate(paint_files):
    image_paths_paint.append(dir_path + '/' + filepath)
    #image_paths_paint.append(filepath)
    if idx == NUM_SKETCH-1:
        break
    if idx % 1000 == 0:
        print idx
print image_paths_paint[0]


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
paint_ids = np.empty(len(image_paths_real), dtype=int)
paint_ids.fill(1)
real_ids = np.empty(len(image_paths_real), dtype=int)
real_ids.fill(0)

data_x = image_paths_real+image_paths_paint
data_y = real_ids.tolist()+paint_ids.tolist()
data = zip(data_x, data_y)
shuffle(data)


# Split data to train/val
with open('val', 'w') as fv, open('train', 'w') as ft, open('imagelist', 'w') as fl:
    for idx, d in enumerate(data):
        if idx <= NUM_VAL-1:
            # Output to file
            fv.write('%s %d\n' % (d[0], d[1]))
        else:
            # Output to file
            ft.write('%s %d\n' % (d[0], d[1]))
        fl.write('%s %d\n' % (d[0], d[1]))

