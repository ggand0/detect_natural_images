# Get data
#paint_path='/home/ispick/Projects/images/single_characters_10000'
paint_path='single_characters_10000'
real_path='real'
paint_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(paint_path) for f in filenames]
real_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(real_path) for f in filenames if os.path.splitext(f)[1] == '.jpg']
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
print len(image_paths_real)


print 'searching paintings...'
print paint_files[0]
for idx, filepath in enumerate(paint_files):
    if not ' ' in filepath:
    	# check if the file is corrupt
    	import cv2
    	img = cv2.imread(filepath, cv2.CV_LOAD_IMAGE_COLOR)
    	if not img is None:
            #image_paths_paint.append(dir_path + '/' + filepath)
            image_paths_paint.append(filepath)
    	else:
    	    print 'corrupt jpg file %s' % filepath
        #image_paths_paint.append(filepath)
    if idx == NUM_SKETCH:
        break
    if idx % 1000 == 0:
        print idx
print image_paths_paint[0]
print len(image_paths_paint)


paint_ids = np.empty(len(image_paths_real), dtype=int)
paint_ids.fill(1)
real_ids = np.empty(len(image_paths_real), dtype=int)
real_ids.fill(0)

data_x = image_paths_real+image_paths_paint
data_y = real_ids.tolist()+paint_ids.tolist(




# train with SVM
from sklearn import datasets
iris = datasets.load_iris()
digits = datasets.load_digits()

from sklearn import svm
clf = svm.SVC(gamma=0.001, C=100.)

clf.fit(digits.data[:-1], digits.target[:-1])
print clf.predict(digits.data[-1:])