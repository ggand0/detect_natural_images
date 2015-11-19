sketch_path='sketch'
real_path='flickr30k-images'
# reshape img array to (rgb, location(1D))
def change_img_array_shape(img_paths, ids):
    result=[]#result=np.array([])
    imgs=[]

    # Load img arrays
    for idx, img_path in enumerate(img_paths):
        if ids[idx] == 0:
            original = Image.open(real_path+'/'+filepath)
            resized = original.resize((IMG_SIZE, IMG_SIZE))
            final_img_arr = np.asarray(resized).flatten().tolist()
            imgs.append(final_img_arr)
        elif ids[idx] == 1:
            original = Image.open('sketch/'+filepath)
            resized = original.resize((IMG_SIZE, IMG_SIZE))
            # Convert grayscale to RGB, since it's read as a grayscale image
            rgbimg = Image.new("RGB", resized.size)
            rgbimg.paste(resized)
            ### transform image to a list of numbers for easy storage.
            final_img_arr = np.asarray(rgbimg).flatten().tolist()
            imgs.append(final_img_arr)

    i=0
    for img in imgs:
        # img = 64,64,3
        index=0
        new_img = [[],[],[]]
        #new_img = np.array([np.array([]),np.array([]),np.array([])])
        for col in img:
            if index % 3 == 0:#R
                #print col

                new_img[0].append(col)
                #print index
                #print new_img[0]
                #np.append(new_img[0], col)

            elif index % 3 == 1:#G
                new_img[1].append(col)
                #np.append(new_img[1], col)
            elif index % 3 == 2:#B
                new_img[2].append(col)
                #np.append(new_img[2], col)
            index += 1

        new_img = np.array(new_img)
        result.append(new_img.reshape(3,64,64))
        #print new_img.shape# => (3, 4096)
        #print new_img.reshape(3,64,64)
        #np.append(result, new_img.reshape(3,64,64))
        i+=1
        if i % 100==0: print i
    return np.array(result)


# Receives all image paths, and yield each mini batch images.
class BatchIterator(object):
    def __init__(self,all_data,all_target,batch_size=100):
        self._data = all_data
        self._target = all_target
        self._n_samples = len(self._target)
        self._i = 0
        self._batch_size = batch_size

        if batch_size > self._n_samples:
            raise Exception("Invalid batch_size !")

        if self._n_samples % batch_size == 0:
            self._batch_num = self._n_samples / batch_size
            print 'debug1', self._batch_num
        else:
            self._batch_num = self._n_samples / batch_size + 1
            print 'debug2', self._batch_num

    def __iter__(self):
        return self

    def next(self):
        if self._i > (self._batch_num -1):
            #self._i = 0
            print 'looped'
            #raise StopIteration
            return None,None

        if self._i == (self._batch_num -1):
            x = self._data[self._i*self._batch_size:]
            y = self._target[self._i*self._batch_size:]
        else:
            #print self._batch_size
            #print self._i*self._batch_size:(self._i+1)*self._batch_size
            x = self._data[self._i*self._batch_size:(self._i+1)*self._batch_size]
            y = self._target[self._i*self._batch_size:(self._i+1)*self._batch_size]

        self._i += 1

        # Convert to img arrays
        return change_img_array_shape(x), change_img_array_shape(y)






