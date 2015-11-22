import os
paint_path='wikipaintings'
paint_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(paint_path) for f in filenames]
print len(paint_files)