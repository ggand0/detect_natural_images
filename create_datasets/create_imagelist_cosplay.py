# -*- coding: utf-8 -*-


# Create a pair of image list file (train/val) for Caffe training
import os
import cv2
import json
import shutil
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot
from PIL import Image
from random import shuffle

NUM_ILLUST=10000
NUM_TRAIN=15000
#NUM_VAL=5000
NUM_VAL=5000
NUM_TEST=5000
K=4 # for corss validation split
illust_path='datasets/illustrations1'
real_path='datasets/cosplay_images_new'
dir_path = os.getcwd()
target_dir=os.path.join(dir_path, 'illust-cosplay_new')

illust_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(illust_path) for f in filenames]
real_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(real_path) for f in filenames]
image_paths_real = []
image_paths_illust = []


print 'searching natural images...'
for idx, filepath in enumerate(real_files):
  img = cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR)
  if not img is None:
    image_paths_real.append(dir_path + '/' + filepath)
  else:
    print 'corrupt jpg file %s' % filepath
  #image_paths_real.append(dir_path + '/' + filepath)
  if len(image_paths_real) == NUM_ILLUST:
    break
  if idx % 1000 == 0:
    print idx
print image_paths_real[0]

print 'searching illustrations...'
for idx, filepath in enumerate(illust_files):
  if not ' ' in filepath:
    # check if the file is corrupt
    '''
    img = cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR)
    if not img is None:
      image_paths_illust.append(dir_path + '/' + filepath)
    else:
      print 'corrupted jpg file: %s' % filepath
    '''
    img = cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR)
    #image_paths_illust.append(dir_path + '/' + filepath)
    if not img is None:
      image_paths_illust.append(dir_path + '/' + filepath)
    else:
      print 'corrupt jpg file %s' % filepath

    if len(image_paths_illust) == NUM_ILLUST:
      break
    if idx % 1000 == 0:
      print idx
print image_paths_illust[0]

print 'length of illusts: %d' % len(image_paths_illust)
print 'length of photos: %d' % len(image_paths_real)


# shuffle data
illust_ids = np.empty(len(image_paths_illust), dtype=int)
illust_ids.fill(1)
real_ids = np.empty(len(image_paths_real), dtype=int)
real_ids.fill(0)
data_x = image_paths_real+image_paths_illust
data_y = real_ids.tolist()+illust_ids.tolist()
data = zip(data_x, data_y)
shuffle(data)


# Split data to train/val
with open('val', 'w') as fv, open('train', 'w') as ft, open('test', 'w') as fl:
  for idx, d in enumerate(data):
    if idx <= NUM_VAL-1:
      # Output to file
      fv.write('%s %d\n' % (d[0], d[1]))
    else:
      # Output to file
      ft.write('%s %d\n' % (d[0], d[1]))
      #fl.write('%s %d\n' % (d[0], d[1]))

