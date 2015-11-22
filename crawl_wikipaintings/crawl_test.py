# using redis ver.
import os
from rq import Queue
from worker import conn
import worker_funcs
q = Queue(connection=conn)
import time

# Create dirs and save images
dir_path = '/Users/pentiumx/Projects/ms_data/wikipainting' # an absolute path is needed

#def save_image(image_url, image_path):
#    img = imread(image_url)
#    matplotlib.image.imsave(image_path, img)

for index in xrange(0,9999):
    name = df.iloc[index]['image_id']
    style = df.iloc[index]['style']
    style_path = dir_path + '/' + style
    # create or get a style dir
    if not os.path.exists(style_path):
        os.makedirs(style_path)
    image_path = style_path+'/'+name
    result = q.enqueue(worker_funcs.save_image, df.iloc[index]['image_url'], image_path)
    time.sleep(0.01)
    if index % 100 == 0:
        print index
print 'DONE!'