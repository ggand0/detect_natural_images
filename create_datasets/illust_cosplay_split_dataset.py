# -*- coding: utf-8 -*-

# ========================================================
#   Split train-val set and save to different directories
#   for training on neon
# ========================================================

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
NUM_VAL=0
NUM_TEST=5000
K=4 # for corss validation split
illust_path='datasets/single_characters_10000'
real_path='datasets/cosplay_images_new'
dir_path = os.getcwd()
target_dir=os.path.join(dir_path, 'illust-cosplay_new')

illust_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(illust_path) for f in filenames]
real_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(real_path) for f in filenames]
image_paths_real = []
image_paths_illust = []


print 'searching natural images...'
for idx, filepath in enumerate(real_files):
  image_paths_real.append(dir_path + '/' + filepath)
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


# Split data to train/val/test sets and save to target dir
for idx, d in enumerate(data):
  if idx < NUM_TRAIN:
    dir_name = 'train'
  elif idx >= NUM_TRAIN and idx < NUM_TRAIN+NUM_VAL:
    dir_name = 'val'
  else:
    dir_name = 'test'

  illust_dir = os.path.join(target_dir, dir_name, 'illust')
  cosplay_dir = os.path.join(target_dir, dir_name, 'cosplay')
  if not os.path.exists(illust_dir):
    os.makedirs(illust_dir)
  if not os.path.exists(cosplay_dir):
    os.makedirs(cosplay_dir)

  filename = os.path.basename(d[0])
  if d[1] == 0: # real
    shutil.copyfile(d[0], os.path.join(cosplay_dir, filename))
  else:         # illust
    shutil.copyfile(d[0], os.path.join(illust_dir, filename))


'''
# shuffle data
data_x = image_paths_real+image_paths_paint
data_y = real_ids.tolist()+paint_ids.tolist()
data = zip(data_x, data_y)
shuffle(data)

with open('%s/val'%target_dir, 'w') as fv, open('%strain'%target_dir, 'w') as ft, open('%stest'%target_dir, 'w') as fl:
  for idx, d in enumerate(data):
    if idx <= NUM_VAL-1:
      fv.write('%s %d\n' % (d[0], d[1]))
    else:
      ft.write('%s %d\n' % (d[0], d[1]))
'''
