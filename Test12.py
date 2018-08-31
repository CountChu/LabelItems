#
# http://answers.opencv.org/question/61105/motion-detection/
#

import cv2
import numpy as np
import time

import LabelItemsCv2

class MotionDetector:

    cam = None
    t_minus = None
    t = None
    t_plus = None

    def __init__ (self, cam):
        self.cam = cam

    grabbed = False
    frame = None

    def readFirstFrame(self):    
        (self.grabbed, self.frame) = self.cam.read()

        self.t_minus = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        self.t = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        self.t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

    diffImage = None    

    def isMotion(self):
        self.diffImage = calculateDiffImg(self.t_minus, self.t, self.t_plus) 


        unique, counts = np.unique(self.diffImage, return_counts=True)
        d = dict(zip(unique, counts))
        
        black = 0
        for i in range (0, 4):
            if i in d.keys():
                black += d[i]
                
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

        (self.grabbed, self.frame) = self.cam.read()       
        self.t_plus = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)

def calculateDiffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

labelItems = LabelItemsCv2.LabelItems(False)

cam = cv2.VideoCapture(0)

#fn = 'IMG_4912.m4v'
#cam = cv2.VideoCapture(fn)

winName = "Movement Indicator"
cv2.namedWindow(winName)


md = MotionDetector(cam)
md.readFirstFrame()

saticCount = 0
lastStatic = False
isStatic = False
labelTrigger = False


while True:

    displayedFrame = None
    #time.sleep(0.01)

    lastStatic = isStatic

    if not md.isMotion():    

        saticCount += 1

        if saticCount >= 10:
            saticCount = 0
            isStatic = True

    else:
        isStatic = False

    labelTrigger = False
    if not lastStatic and isStatic:
        labelTrigger = True

    title = "lastStatic = %d, isStatic = %d, labelTrigger = %d" % (lastStatic, isStatic, labelTrigger)

    if labelTrigger:       


        labelItems.handleImage(md.frame, True)

        displayedFrame = labelItems.finalImage

    if not isStatic:
        displayedFrame = md.frame


    '''
    cv2.putText (
        md.diffImage, 
        'STATIC',
        (10, md.diffImage.shape[0] - 10), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        10, 
        (125, 125, 125), 
        4) 
    '''

    if displayedFrame != None:

        cv2.putText (
            displayedFrame, 
            title,
            (10, displayedFrame.shape[0] - 10), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            2, 
            (0, 255, 0), 
            4) 

        cv2.imshow("Final", displayedFrame)    

    #cv2.imshow("Original", md.frame)
    
    #cv2.imshow("Black", labelItems.blackImage)
    #cv2.imshow("White", labelItems.whiteImage)

    #cv2.imshow(winName, md.diffImage)

    # Read next image
    md.readNextFrame()

    key = cv2.waitKey(10)
    if key == 27:                       # ESC
        cv2.destroyWindow(winName)
        break      

print ("Goodbye")