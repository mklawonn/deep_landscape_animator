import cv2
import errno
from os import listdir, makedirs
from os.path import isfile, isdir, join, exists




directories = [f for f in listdir("./data/") if isdir(join("./data/", f))]

print len(directories)

for d in directories:
    path = "./data/{0}/".format(d)
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f in onlyfiles:
        vidcap = cv2.VideoCapture("{0}{1}".format(path, f))
        directory = "{0}{1}_frames/".format(path, f)
        if not exists(directory):
            try:
                makedirs(directory)
            except OSError as exception:
                print "ERROR!"
                if exception.errno != errno.EEXIST:
                    raise
        success,image = vidcap.read()
        count = 0
        success = True
        print "Writing {0}".format(directory)
        while success:
            success,image = vidcap.read()
            #print 'Read a new frame: ', success
            if success:
                cv2.imwrite("{0}frame{1}.jpg".format(directory, count), image)     # save frame as JPEG file
                count += 1
