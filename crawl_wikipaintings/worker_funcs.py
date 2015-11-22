"""import matplotlib
from skimage.io import imread, imshow
def save_image(image_url, image_path):
    img = imread(image_url)
    matplotlib.image.imsave(image_path, img)"""

import urllib

def save_image(image_url, image_path):
	#urllib.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")
	urllib.urlretrieve(image_url, image_path)