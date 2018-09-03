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
    print ("        -f, --file")
    print ("            input.avi")
    print ("        -a, --algorithm")  
    print ('            a1, Cv2')
    print ('            a2, Ski')
    print ("        -o, --output")      
    print ("            output.avi")
    print ("        -t, --transform")  

def main():

    #
    # Parse arguments.
    #

    cfg = {
        'h': False,
        'd': False,
        'f': '',
        'a': 'a1',        
        'o': '',
        't': False}

    try:
        (opts, args) = getopt.getopt(
            sys.argv[1:], 
            'hdf:a:o:t',
            ['help', 'debug', 'file', 'algorithm', 'output', 'transform'])
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(0)

    print (opts)        
        
    for o, a in opts:
        if o in ('-h', '--help'):
            cfg['h'] = True
        elif o in ('-d', '--debug'):
            cfg['d'] = True
        elif o in ('-f', '--file'):
            cfg['f'] = a
        elif o in ('-a', '--algorithm'):
            cfg['a'] = a
        elif o in ('-o', '--output'):            
            cfg['o'] = a
        elif o in ('-t', '--transform'):            
            cfg['t'] = True
        else:
            help()
            sys.exit(0)

    if cfg['h']:
        help()
        sys.exit(0)     

    #
    # Build a LabelImage object.
    #

    if cfg['a'] == 'a1':
        labelImage = LabelImageCv2.LabelImage(True)           
    elif cfg['a'] == 'a2':
        labelImage = LabelImageSki.LabelImage(True)        
    else:
        help()
        sys.exit(0)

    #
    # Open file or camera.
    #    
    
    if cfg['f'] != '':
        cam = cv2.VideoCapture(cfg['f'])
    else:
        cam = cv2.VideoCapture(0)

    if cfg['o'] != '':
        outputFn = cfg['o']
        (grabbed, frame) = cam.read()
        (fheight, fwidth, _) = frame.shape
        print (fwidth , fheight)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(outputFn,fourcc, 20.0, (fwidth, fheight))

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

        labeledImage = None
        transformedImage = None
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

        labelImage.processImages = []
        if labelTrigger:
        
            if cfg['t']:
            
                #
                # Find max contour.
                #

                maxApprox = labelImage.getMaxApprox(md.frame)
                labeledImage = labelImage.getProcessImage('2 Before Original')
                
                '''
                if maxApprox is not None: 
                    transformedImage = labelImage.transform(md.frame, maxApprox)

                    #
                    # Label the transformed image.
                    #    

                    #labelImage.handle(transformedImage, True)
                    #displayedFrame = labelImage.finalImage
                    #whiteFrame = labelImage.whiteImage
                '''
                    
            else:

                labelImage.handle(md.frame, False)
                displayedFrame = labelImage.finalImage
                whiteFrame = labelImage.whiteImage

        if not isStatic:
            displayedFrame = md.frame
            whiteFrame = md.frame.copy()
            whiteFrame.fill(255)
            
        if cfg['t']:    
            if transformedImage is not None:
                cv2.imshow("Transform", transformedImage)   
                
        if labeledImage is not None:
            cv2.imshow("2 Before Original", labeledImage)  
            
        if displayedFrame is not None:

            cv2.putText (
                displayedFrame, 
                title,
                (10, displayedFrame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                (0, 255, 0), 
                2) 

            cv2.imshow("Final", displayedFrame)   

            if cfg['o']:
                out.write(displayedFrame) 

        if whiteFrame is not None:
            cv2.imshow("White", whiteFrame)

        #cv2.imshow("Original", md.frame)        
        #cv2.imshow("Black", labelImage.blackImage)
        #cv2.imshow(winName, md.diffImage)

        #
        # Read next frame
        #

        md.readNextFrame()

        key = cv2.waitKey(50) # wait 50 milliseconds before each frame is written.
        if key == 27:                       # ESC
            cv2.destroyWindow(winName)
            break      

    if cfg['o']:
        out.release()


    print ("Goodbye")

if __name__ == '__main__':
    main()    