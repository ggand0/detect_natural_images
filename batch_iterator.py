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

        return x,y


