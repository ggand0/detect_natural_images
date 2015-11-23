import csv


EXTRACT_NUM=50000
with open('wikipaintings_oct2013.csv', 'rb') as f:
    reader = csv.reader(f)
    df = list(reader)

#print data_frames[:5]
print df[1][5]
print df[1][10]
image_id_idx=0
style_idx=5
image_url_idx=10


# using redis ver.
import os
from rq import Queue
from worker import conn
import worker_funcs
q = Queue(connection=conn)
import time

# Create dirs and save images
#dir_path = '/home/ispick/Projects/illust_detection/detect_natural_images/wikipaintings' # an absolute path is needed
dir_path = '/home/ubuntu/Projects/detect_natural_images/wikipaintings' # an absolute path is needed

#def save_image(image_url, image_path):
#    img = imread(image_url)
#    matplotlib.image.imsave(image_path, img)

for index in xrange(1,EXTRACT_NUM):# since raw 0 has headers
    name = df[index][image_id_idx]
    style = df[index][style_idx]
    style_path = dir_path + '/' + style
    # create or get a style dir
    if not os.path.exists(style_path):
        os.makedirs(style_path)
    image_path = style_path+'/'+name
    result = q.enqueue(worker_funcs.save_image, df[index][image_url_idx], image_path)
    time.sleep(0.01)
    if index % 100 == 0:
        print index
print 'DONE!'
