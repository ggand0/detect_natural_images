from neon.data import DataIterator
import numpy as np

"""
X is the input features and y is the labels.
Here, we show how to load in 10,000 images that each have height and width
of 32, and 3 channels (R,G,B)
The data in X has to be laid out as follows: (# examples, feature size)
The labels y have the same first dimension as the number of examples
(in the case of an autoencoder, we do not specify y).
"""

X = np.random.rand(10000,3072)
y = np.random.randint(1,11,10000)
print X.shape
print y.shape

"""
We pass the data points and labels X, y to be loaded into the backend
We set nclass to 10, for 10 possible labels
We set lshape to (3,32,32), to represent the 32x32 image with 3 channels
"""

train = DataIterator(X=X, y=y, nclass=10, lshape=(3,32,32))