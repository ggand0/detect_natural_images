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
real_path='flickr30k-images'
sketch_files = [ f for f in listdir(sketch_path) if isfile(join(sketch_path,f)) ]
real_files = [ f for f in listdir(real_path) if isfile(join(real_path,f)) ]
sketch_dirs = [x[0] for x in os.walk(sketch_path)]
lines=[]
with open('sketch/filelist.txt') as f:
    lines = f.read().splitlines()


print 'resizing real images...'
for idx, filepath in enumerate(real_files):
    original = Image.open(real_path+'/'+filepath)
    resized = original.resize((IMG_SIZE, IMG_SIZE))
    #print np.asarray(resized).shape
    final_img_arr = np.asarray(resized).flatten().tolist()
    #print len(final_img_arr)
    cleaned_imgs_real.append(final_img_arr)
    if idx == NUM_SKETCH:
        break
    if idx % 100 == 0:
        print idx


print 'resizing sketches...'
for idx, filepath in enumerate(lines):
    #print filepath
    original = Image.open('sketch/'+filepath)
    resized = original.resize((IMG_SIZE, IMG_SIZE))
    #resized = cv2.cvtColor(resized, cv.CV_GRAY2RGB)

    # Convert grayscale to RGB, since it's read as a grayscale image
    rgbimg = Image.new("RGB", resized.size)
    rgbimg.paste(resized)
    #print np.asarray(rgbimg).shape

    ### transform image to a list of numbers for easy storage.
    final_img_arr = np.asarray(rgbimg).flatten().tolist()

    ###append data to lists
    cleaned_imgs_sketch.append(final_img_arr)
    if idx == NUM_SKETCH:
        break

    if idx % 100 == 0:
        print idx
#print 'cleaned_imgs: %s' % len(cleaned_imgs_sketch)

sketch_ids = np.empty(len(cleaned_imgs_sketch))
real_ids = np.empty(len(cleaned_imgs_real))
sketch_ids.fill(1)
real_ids.fill(0)

train_data={
    "imgs":cleaned_imgs_real+cleaned_imgs_sketch,
    "ids":real_ids.tolist()+sketch_ids.tolist()
    #"names":whale_names
}
with open("./nn_train_data.json","w") as f:
    json.dump(train_data,f)
