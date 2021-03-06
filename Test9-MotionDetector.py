#
# http://answers.opencv.org/question/61105/motion-detection/
#

import cv2
import numpy as np
import time

class MotionDetector:

    cam = None
    t_minus = None
    t = None
    t_plus = None

    def __init__ (self, cam):
        self.cam = cam

    def readFirstFrame(self):    
        self.t_minus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        self.t = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        self.t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

    diffImage = None    

    def isMotion(self):
        self.diffImage = calculateDiffImg(self.t_minus, self.t, self.t_plus) 


        unique, counts = np.unique(self.diffImage, return_counts=True)
        d = dict(zip(unique, counts))
        #print (d)
        black = d[0] + d[1] + d[2] + d[3]
        sum = 0
        for unique, counts in d.items():
            sum += counts
        rate = black/sum
        print (rate)

        res = True
        if rate >= 0.95:
            res = False

        return res    

    def readNextFrame(self):
        self.t_minus = self.t
        self.t = self.t_plus
        self.t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

def calculateDiffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

#cam = cv2.VideoCapture(0)

fn = 'IMG_4912.m4v'
cam = cv2.VideoCapture(fn)

winName = "Movement Indicator"
cv2.namedWindow(winName)


md = MotionDetector(cam)
md.readFirstFrame()

while True:

    time.sleep(0.01)

    if not md.isMotion():    
        cv2.putText (
            md.diffImage, 
            'STATIC',
            (10, md.diffImage.shape[0] - 10), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            10, 
            (125, 125, 125), 
            4)   

    cv2.imshow(winName, md.diffImage)

    # Read next image
    md.readNextFrame()

    key = cv2.waitKey(10)
    if key == 27:                       # ESC
        cv2.destroyWindow(winName)
        break      

print ("Goodbye")