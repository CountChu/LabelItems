import sys
import getopt

import cv2
import numpy as np
import time

import LabelImageSki
import LabelImageCv2
import MotionDetector

def help():
    print ("Usage:")
    print ("    python TestLabelVideo.py")    
    print ("        -h, --help") 
    print ("        -d, --debug")      
    print ("        -a, --algorithm")  
    print ('            a1, Ski')
    print ('            a2, Cv2')

def main():


    #
    # Parse arguments.
    #

    cfg = {
        'h': False,
        'd': False,
        'a': 'a1'}

    try:
        (opts, args) = getopt.getopt(
            sys.argv[1:], 
            "hda:",
            ["help", "debug", "algorithm"])
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(0)
        
    for o, a in opts:
        if o in ('-h', '--help'):
            cfg['h'] = True
        elif o in ('-d', '--debug'):
            cfg['d'] = True
        elif o in ('-a', '--algorithm'):
            cfg['a'] = a
        else:
            help()
            sys.exit(0)

    print (opts)

    if cfg['h']:
        help()
        sys.exit(0)     

    #
    # Build a LabelImage object.
    #

    if cfg['a'] == 'a1':
        labelImage = LabelImageSki.LabelImage(False)           
    elif cfg['a'] == 'a2':
        labelImage = LabelImageCv2.LabelImage(False)        
    else:
        help()
        sys.exit(0)

    #
    # Open camera.
    #    


    cam = cv2.VideoCapture(0)

    #fn = 'IMG_4912.m4v'
    #cam = cv2.VideoCapture(fn)

    winName = "Movement Indicator"
    cv2.namedWindow(winName)


    md = MotionDetector.MotionDetector(cam)
    md.readFirstFrame()

    saticCount = 0
    lastStatic = False
    isStatic = False
    labelTrigger = False


    while True:

        displayedFrame = None
        whiteFrame = None 
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


            labelImage.handleImage(md.frame, True)

            displayedFrame = labelImage.finalImage
            whiteFrame = labelImage.whiteImage

        if not isStatic:
            displayedFrame = md.frame
            whiteFrame = md.frame.copy()
            whiteFrame.fill(255)

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

        if whiteFrame != None:    
            cv2.imshow("White", whiteFrame)

        #cv2.imshow("Original", md.frame)        
        #cv2.imshow("Black", labelImage.blackImage)
        #cv2.imshow(winName, md.diffImage)

        #
        # Read next frame
        #

        md.readNextFrame()

        key = cv2.waitKey(10)
        if key == 27:                       # ESC
            cv2.destroyWindow(winName)
            break      

    print ("Goodbye")


if __name__ == '__main__':
    main()    