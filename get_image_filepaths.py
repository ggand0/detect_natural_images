# -*- coding: utf-8 -*-
import os
import json
from matplotlib import pyplot
import numpy as np
from PIL import Image
import pandas as pd
from os import listdir
from os.path import isfile, join
#import cv
#import cv2

cleaned_imgs_real=[]
cleaned_imgs_sketch=[]
whale_ids=[]
whale_names=[]


IMAGE_PER_CLASS=5
NUM_SKETCH=10000
IMG_SIZE=256#64
sketch_path='sketch'
real_path='real'
sketch_files = [ f for f in listdir(sketch_path) if isfile(join(sketch_path,f)) ]
#real_files = [ f for f in listdir(real_path) if isfile(join(real_path,f)) ]
import os
real_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(real_path) for f in filenames if os.path.splitext(f)[1] == '.jpg']
sketch_dirs = [x[0] for x in os.walk(sketch_path)]
lines=[]
with open('sketch/filelist.txt') as f:
    lines = f.read().splitlines()


print 'searching real images...'
for idx, filepath in enumerate(real_files):
    cleaned_imgs_real.append(filepath)
    if idx == NUM_SKETCH:
        break
    if idx % 1000 == 0:
        print idx


print 'searching sketches...'
for idx, filepath in enumerate(lines):
    ###append data to lists
    cleaned_imgs_sketch.append(filepath)
    if idx == NUM_SKETCH:
        break
    if idx % 1000 == 0:
        print idx


sketch_ids = np.empty(len(cleaned_imgs_sketch))
real_ids = np.empty(len(cleaned_imgs_real))
sketch_ids.fill(1)
real_ids.fill(0)

#print real_ids.tolist()+sketch_ids.tolist()

train_data={
    "imgs":cleaned_imgs_real+cleaned_imgs_sketch,
    "ids":real_ids.tolist()+sketch_ids.tolist()
}
with open("./nn_train_data_paths.json","w") as f:
    json.dump(train_data,f)