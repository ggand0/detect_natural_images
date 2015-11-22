# Modified from cifar10_cnn.py

from __future__ import absolute_import
from __future__ import print_function
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils
from six.moves import range

import numpy as np
import sys
import illust_dataset as wd
from batch_iterator import BatchIterator


'''
    Train a (fairly simple) deep CNN on the CIFAR10 small images dataset.

    GPU run command:
        THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python cifar10_cnn.py

    It gets down to 0.65 test logloss in 25 epochs, and down to 0.55 after 50 epochs.
    (it's still underfitting at that point, though).

    Note: the data was pickled with Python 2, and some encoding issues might prevent you
    from loading it in Python 3. You might have to load it in Python 2,
    save it in a different format, load it in Python 3 and repickle it.
'''

batch_size = 32#32
nb_classes = 2#450
nb_epoch = 2#10#50
data_augmentation = False#True

# input image dimensions
IMG_SIZE=128
img_rows, img_cols = IMG_SIZE,IMG_SIZE
# the CIFAR10 images are RGB
img_channels = 3

# the data, shuffled and split between tran and test sets
(X_train, y_train), (X_test, y_test) = wd.load_data()
print('X_train shape:', X_train.shape)
print(y_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
#Y_train = np_utils.to_categorical(y_train, nb_classes)
#Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

model.add(Convolution2D(32, 3, 3, border_mode='full',
                        #input_shape=(img_rows, img_cols, img_channels)))
                        input_shape=(img_channels, img_rows, img_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='full'))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# let's train the model using SGD + momentum (how original).
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
adagrad = Adagrad(lr=0.01, epsilon=1e-6)
model.compile(loss='categorical_crossentropy', optimizer=adagrad)

#X_train = X_train.astype("float32")
#X_test = X_test.astype("float32")
#X_train /= 255
#X_test /= 255

if not data_augmentation:
    print("Not using data augmentation or normalization")
    #model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch)
    # Alternatively, let's say you have a MiniBatchGenerator that yields 32-64 samples at a time:
    for e in range(nb_epoch):
        print("epoch %d" % e)
        #DEBUG
        #X_train = X_train[:35]
        #y_train = y_train[:35]
        #X_train = X_train[:5000]
        #y_train = y_train[:5000]
        b = BatchIterator(X_train, y_train, batch_size)
        X_batch, Y_batch = b.next()
        #print(X_batch[0])
        #print(Y_batch[0])

        num=0
        progbar = generic_utils.Progbar(len(X_train))
        while X_batch is not None:# and Y_batch != None:
            X_batch, Y_batch = b.next()
            #print(Y_batch)

            try:
                X_batch = X_batch.astype("float32")
            except AttributeError as e:
                print (e)
                print (X_batch)
                print(type(X_batch))
                break
            X_batch /= 255
            # convert class vectors to binary class matrices
            Y_batch = np_utils.to_categorical(Y_batch, nb_classes)
            #print(Y_batch[0])

            loss, acc = model.train_on_batch(X_batch, Y_batch, accuracy=True)
            progbar.add(batch_size, values=[("train loss", loss), ("train acc", acc)])
            #num += 1
            #if num % 10 == 0:
            #    print ( str(num*batch_size) + 'out of %d' % len(X_train) + ' loss:%f'%loss )


            #model.fit(X_batch, Y_batch)
        #for X_train, Y_train in BatchIterator(): # these are chunks of ~10k pictures
        #    model.train(X_batch, Y_batch)

    #score = model.evaluate(X_test, Y_test, batch_size=batch_size)
    # Load images before calling to_categorical
    X_test = wd.load_test_images(X_test, y_test)
    print(len(X_test))

    # convert class vectors to binary class matrices
    Y_test = np_utils.to_categorical(y_test, nb_classes)
    X_test = np.array(X_test).astype("float32")
    X_test /= 255
    print(X_test.shape)
    print(Y_test.shape)
    score, acc = model.evaluate(X_test, Y_test, show_accuracy=True, batch_size=batch_size)
    print('Test score:', score)
    print('Test acc:', acc)

else:
    print("Using real time data augmentation")


    # this will do preprocessing and realtime data augmentation
    datagen = ImageDataGenerator(
        featurewise_center=True,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=True,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=20,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.2,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    # compute quantities required for featurewise normalization
    # (std, mean, and principal components if ZCA whitening is applied)
    datagen.fit(X_train)

    for e in range(nb_epoch):
        print('-'*40)
        print('Epoch', e)
        print('-'*40)
        print("Training...")
        # batch train with realtime data augmentation
        progbar = generic_utils.Progbar(X_train.shape[0])
        for X_batch, Y_batch in datagen.flow(X_train, Y_train):
            loss = model.train_on_batch(X_batch, Y_batch)
            progbar.add(X_batch.shape[0], values=[("train loss", loss)])

        print("Testing...")
        # test time!
        progbar = generic_utils.Progbar(X_test.shape[0])
        for X_batch, Y_batch in datagen.flow(X_test, Y_test):
            score = model.test_on_batch(X_batch, Y_batch)
            progbar.add(X_batch.shape[0], values=[("test loss", score)])
