import cv2
vidcap = cv2.VideoCapture('test.mp4')
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  #print 'Read a new frame: ', success
  if success:
      cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
      count += 1
