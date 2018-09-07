#
# https://pythontips.com/2015/03/11/a-guide-to-finding-books-in-images-using-python-and-opencv/
#

import numpy as np
import cv2
import matplotlib.pyplot as plt

class LabelImage:

    keepProcess = False

    def __init__ (self, keepProcess):
        self.keepProcess = keepProcess   

    def getProcessImage(self, foundTitle):
        for pi in self.processImages:
            (title, image, canSave) = pi
            if title == foundTitle:
                return image
        return None
        
    def getMaxApprox(self, image):
    
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.

        if self.keepProcess:
            self.processImages.append(('1 Before Original', image, False))        
        
        #
        # Convert the image to grayscale, and blur it
        #
        
        grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        grayImage = cv2.GaussianBlur(grayImage, (3, 3), 0)
        
        #
        # detect edges in the gray image
        #

        edgedImage = cv2.Canny(grayImage, 10, 250) 
        #edgedImage = cv2.Canny(grayImage, 200, 250) 

        #
        # construct and apply a closing kernel to 'close' gaps between 'white'
        # pixels
        #

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closedImage = cv2.morphologyEx(edgedImage, cv2.MORPH_CLOSE, kernel)

        #
        # find contours (i.e. the 'outlines') in the image and initialize the
        # total number of books found
        #

        (_, cnts, _) = cv2.findContours(closedImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total = 0

        #
        # loop over the contours
        #

        if self.keepProcess:
            labeledImage = image.copy()
            self.processImages.append(('2 Before Original', labeledImage, False))    

        maxC = None
        maxApprox = None
        maxAreaSize = 0
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

            if len(approx) == 4:
            #if len(approx) <= 8:
                areaSize = cv2.contourArea(c)
                if areaSize > maxAreaSize:
                    maxAreaSize = areaSize
                    maxC = c
                    maxApprox = approx
                print ("It is candidated. areaSize = %d" % areaSize)
                if self.keepProcess:
                    thin = 5
                    cv2.drawContours(labeledImage, [approx], -1, (0, 0, 255), thin)
                total += 1
        
        if self.keepProcess:
            if maxApprox is not None:
                thin = 20    
                cv2.drawContours(labeledImage, [maxApprox], -1, (0, 255, 0), thin)

        print ("maxApprox = %s, maxAreaSize = %d" % (maxApprox, maxAreaSize))
        #if maxAreaSize <= 10000:
        if maxAreaSize <= 30000:
            print ("Skip it.")
            return None
            
        return maxApprox

    def transform(self, image, maxApprox, width, height):

        thin = 20    

        #
        # Perspective transform.
        #

        pts1 = np.float32([maxApprox[0], maxApprox[1], maxApprox[2], maxApprox[3]])
        pts2 = np.float32([
                [width ,0],
                [0, 0],
                [0, height],
                [width, height]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        transformedImage = cv2.warpPerspective(image, M, (width, height))
        
        return transformedImage

        
    processImages = []     

    finalImage = None
    blackImage = None
    whiteImage = None

    def handle(self, image, doTransfer):

        if doTransfer:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.

        if self.keepProcess:
            self.processImages.append(('Original', image, False))

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
        
        sizeList = ""
        for c in cnts:
            areaSize = cv2.contourArea(c)
            sizeList += str(areaSize) + ", "
        print(sizeList)
        
        for c in cnts:
        
            areaSize = cv2.contourArea(c)
            if areaSize <= 10000:
                continue
        
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
            if len(approx) <= 10:  # 8
                thin = 5
                cv2.drawContours(self.finalImage, [approx], -1, (0, 255, 0), thin)
                cv2.drawContours(self.blackImage, [approx], -1, (0, 255, 0), thin)
                cv2.drawContours(self.whiteImage, [approx], -1, (0, 255, 0), thin)
                total += 1
                
        #    
        # display the output
        #

        print ("I found {0} books in that finalImage".format(total))

        if self.keepProcess:        
            self.processImages.append(('Final', self.finalImage, True))   
            self.processImages.append(('Black', self.blackImage, True))     
            self.processImages.append(('White', self.whiteImage, True)) 
        


