#
# http://answers.opencv.org/question/61105/motion-detection/
#

import cv2
import numpy as np

def calculateDiffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)

winName = "Movement Indicator"
cv2.namedWindow(winName)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while True:

    diffImage = calculateDiffImg(t_minus, t, t_plus) 


    unique, counts = np.unique(diffImage, return_counts=True)
    d = dict(zip(unique, counts))
    #print (d)
    sum = d[0] + d[1] + d[2] + d[3]
    print (sum)

    isStatic = False
    if sum >= 800000:
        isStatic = True

    if isStatic:    
        cv2.putText (
            diffImage, 
            'STATIC',
            (10, diffImage.shape[0] - 10), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            10, 
            (125, 125, 125), 
            4)   

    cv2.imshow(winName, diffImage)

    # Read next image
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    key = cv2.waitKey(10)
    if key == 27:                       # ESC
        cv2.destroyWindow(winName)
        break      

print ("Goodbye")