#
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4081273/
#

import cv2
from skimage import data, io, filters
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import skimage.feature
import skimage.morphology
import skimage.measure

def overlappedSegment(x1, x2, x3, x4):
    if max(x1, x2) - min(x3, x4) >= 0 and max(x3, x4) - min(x1, x2) >= 0:
        return True
    return False

def overlappedArea(box1, box2):
    print (box1)
    print (box2)
    (x1, y1, x2, y2) = box1
    (x3, y3, x4, y4) = box2
    if overlappedSegment(x1, x2, x3, x4) and overlappedSegment(y1, y2, y3, y4):
        return True

    return False

def mergeArea(box1, box2):
    (x1, y1, x2, y2) = box1
    (x3, y3, x4, y4) = box2
    newX1 = min(x1, x2, x3, x4)
    newX2 = max(x1, x2, x3, x4)
    newY1 = min(y1, y2, y3, y4)
    newY2 = max(y1, y2, y3, y4)
    return (newX1, newY1, newX2, newY2)

def findOverlappedRegions(boxList):
    for i in range(0, len(boxList) - 1):
        for j in range(1, len(boxList)):
            if i < j:
                #print ("%d, %d" % (i, j))
                [box1, merged1] = boxList[i]
                [box2, merged2] = boxList[j]
                if not merged1 and not merged2:
                    if overlappedArea(box1, box2):
                        return (i, j)
    return None    

def getArea(box):
    (x1, y1, x2, y2) = box
    area = abs(x1-x2+1) * abs(y1-y2+1)
    return area

def labelImage(boxList, image):
    newImage = image.copy()
    count = 0
    for box in boxList:

        print ("box = ", str(box))
        
        #
        # Draw rectangle around segmented objects.
        #

        minr, minc, maxr, maxc = box

        cv2.rectangle (
            newImage,
            (minc, minr),
            (maxc, maxr),
            (0, 255, 0),
            4)
        
        count += 1

    print ("count = ", count) 
    return newImage


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

    def handleImage(self, image, doTransfer):

        if doTransfer:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.
        
        if self.keepProcess:
            self.processImages.append(('Orignal', image, False))

        #
        # get grayed image.
        #


        image1 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # RGB to GRAY, ndim = 2
        if self.keepProcess: 
            self.processImages.append(('Gray', image1, True))

        #
        # Get edges.
        #

        edges = skimage.feature.canny(
                  image1, 
                  sigma=2, # 3
                  low_threshold=0, # 10
                  high_threshold=15) # 80
        #edges = canny(image1, sigma=2)
        #cv2.imwrite(dstFn2, edges)
        if self.keepProcess:        
            self.processImages.append(('Edges', edges, False))        

        #
        # Label image.
        #

        label_image = skimage.morphology.label(edges)          # ndarray   

        if self.keepProcess:
            boxList = [region.bbox for region in skimage.measure.regionprops(label_image)]
            image3 = labelImage(boxList, image)
            self.processImages.append(('Labeled Items', image3, True))


        #
        # Filter regions.
        #

        maxRegionArea = 0
        for region in skimage.measure.regionprops(label_image):
            regionArea = getArea(region.bbox)
            maxRegionArea = max(maxRegionArea, regionArea)
        print ("maxRegionArea = ", maxRegionArea)

        boxList4 = []
        count = 0
        imageArea = image.shape[0] * image.shape[1]
        for region in skimage.measure.regionprops(label_image):
            if region.area <= 70:
                continue
            
            #
            # 503 * 377
            # image.shape = 504 * 378 = 190512
            #

            regionArea = getArea(region.bbox)
            if regionArea > imageArea * 0.9:
                print ("regionArea = ", regionArea)
                print ("imageArea = ", imageArea)
                continue
            count += 1    
            print ("region = %s, %s" % (region.area, region.bbox))
            boxList4.append(region.bbox)      
        
        if self.keepProcess:
            image4 = labelImage(boxList4, image)     
            self.processImages.append(('Labeled Items Filtered', image4, True))


        #
        # Transform boxList4 to boxFlagList
        #     

        boxFlagList = []
        for box in boxList4:
            boxFlagList.append([box, False])

        #
        # merge overlapped boxFlagList.
        #    

        while True:
            result = findOverlappedRegions(boxFlagList)
            if result == None:
                break

            (i, j) = result
            [box1, merged1] = boxFlagList[i]
            [box2, merged2] = boxFlagList[j]
            box = mergeArea(box1, box2)
            print ("box = %s" % str(box))
            boxFlagList[i][1] = True
            boxFlagList[j][1] = True
            boxFlagList.append([box, False])

        for box in boxFlagList:
            print(box)

        boxList5 = []
        for [box, merged] in boxFlagList:
            if merged:
                continue
            boxList5.append(box)   

        #
        # If keepProess, label items on the original image. 
        #     

        if self.keepProcess:
            image5 = labelImage(boxList5, image)
            self.processImages.append(('Labeled Items Merged', image5, True))
  

        #
        # Output regions in a background image.
        #

        image6 = image.copy()
        image6.fill(0)
        image6 = labelImage(boxList5, image6)   
        if self.keepProcess:         
            self.processImages.append(('Labeled Items Black', image6, True))

        image7 = image.copy()
        image7.fill(255)
        image7 = labelImage(boxList5, image7)    
        if self.keepProcess:        
            self.processImages.append(('Labeled Items White', image7, True))