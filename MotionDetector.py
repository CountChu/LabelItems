import cv2
import numpy as np

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
        i = 0
        for unique in sorted(d):
            i += 1
            black += d[unique]
            if i == 4:
                break

        sum = 0
        for unique, counts in d.items():
            sum += counts
        rate = black/sum
        print (rate)

        res = True
        if rate >= 0.98:
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