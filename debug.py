from batch_iterator import BatchIterator

x=[1,2,3]
y=[1,2,3]
b=BatchIterator(x,y,1)
print b.next()
print b.next()
print b.next()
print b.next()