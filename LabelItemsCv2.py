#
# https://pythontips.com/2015/03/11/a-guide-to-finding-books-in-images-using-python-and-opencv/
#

import numpy as np
import cv2
import matplotlib.pyplot as plt

class LabelItems:

    keepProcess = False

    def __init__ (self, keepProcess):
        self.keepProcess = keepProcess    

    def handleFile(self, fn):

        #
        # Load a JPG image file.
        #

        image = cv2.imread(fn)     # numpy.ndarray, ndim = 3
        self.handleImage(image, True)

    processImages = []     

    finalImage = None
    blackImage = None
    whiteImage = None

    def handleImage(self, image, doTransfer):

        if doTransfer:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.

        if self.keepProcess:
            self.processImages.append(('Orignal', image, False))

        #
        # get grayed blured image.
        #


        grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        grayImage = cv2.GaussianBlur(grayImage, (3, 3), 0)   

        if self.keepProcess: 
            self.processImages.append(('Gray and Blur', grayImage, True))

        #
        # detect edges in the image
        #

        edgedImage = cv2.Canny(grayImage, 10, 250)
        #edgedImage = cv2.Canny(grayImage, 10, 20)

        if self.keepProcess:        
            self.processImages.append(('Edged', edgedImage, False)) 

        #
        # construct and apply a closing kernel to 'close' gaps between 'white'
        # pixels
        #

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closedImage = cv2.morphologyEx(edgedImage, cv2.MORPH_CLOSE, kernel)

        if self.keepProcess:        
            self.processImages.append(('Closed', closedImage, True)) 

        #
        # find contours (i.e. the 'outlines') in the image and initialize the
        # total number of books found
        #

        (_, cnts, _) = cv2.findContours(closedImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total = 0

        #
        # loop over the contours
        #

        self.finalImage = image.copy()
        
        self.blackImage = image.copy()
        self.blackImage.fill(0)
        
        self.whiteImage = image.copy()
        self.whiteImage.fill(255)
        
        for c in cnts:
        
            #print ("c = %s" % c)
         
            #
            # approximate the contour
            #
            
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            print ("len(approx) = ", len(approx))

            #
            # if the approximated contour has four points, then assume that the
            # contour is a book -- a book is a rectangle and thus has four vertices
            #
            
            #if len(approx) == 4:
            if len(approx) <= 8:
                cv2.drawContours(self.finalImage, [approx], -1, (0, 255, 0), 4)
                cv2.drawContours(self.blackImage, [approx], -1, (0, 255, 0), 4)
                cv2.drawContours(self.whiteImage, [approx], -1, (0, 255, 0), 4)
                total += 1
                
        #    
        # display the output
        #

        print ("I found {0} books in that finalImage".format(total))

        if self.keepProcess:        
            self.processImages.append(('Final', self.finalImage, True))   
            self.processImages.append(('Black', self.blackImage, True))     
            self.processImages.append(('White', self.whiteImage, True)) 
        


