#
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4081273/
#

import cv2
from skimage import data, io, filters
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import getopt

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

def help():
    print ("Usage:")
    print ("    python LabelItems.py IMG_4889.jpg -s")    
    print ("        -h, --help")
    print ("        -s, --show")   
    print ("        -p, --process")      

def main():

    if len(sys.argv) <= 1:
        help()
        sys.exit(0)

    fn = sys.argv[1]

    #
    # Prepare file names of output
    #
    
    (dstFn, ext) = os.path.splitext(fn);
    
    processFn = dstFn + "-Process" + ext
    print ("processFn = "+processFn)

    dstFn1 = dstFn + "-1" + ext
    dstFn2 = dstFn + "-2" + ext
    dstFn3 = dstFn + "-3" + ext
    dstFn4 = dstFn + "-4" + ext
    dstFn5 = dstFn + "-5" + ext  
    dstFn6 = dstFn + "-6" + ext   
    dstFn7 = dstFn + "-7" + ext                         

    #
    # Parse arguments.
    #

    cfg = {
        'h': False,
        's': False,
        'p': False}

    try:
        (opts, args) = getopt.getopt(
            sys.argv[2:], 
            "hsp",
            ["help", "show", "process"])
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(0)
        
    for o, a in opts:
        if o in ('-h', '--help'):
            cfg['h'] = True
        elif o in ('-p', '--process'):
            cfg['p'] = True
        elif o in ('-s', '--show'):
            cfg['s'] = True
        else:
            help()
            sys.exit(0)

    #
    # Load a JPG image file.
    #

    image = cv2.imread(fn)     # numpy.ndarray, ndim = 3
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.
    
    #
    # get grayed image.
    #


    image1 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # RGB to GRAY, ndim = 2


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

    #
    # Label image.
    #

    label_image = skimage.morphology.label(edges)          # ndarray    

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
    # Label image finally.
    #    

    image5 = labelImage(boxList5, image)
    cv2.imwrite(dstFn5, image5)   

    #
    # Output regions in a background image.
    #

    image6 = image.copy()
    image6.fill(0)
    image6 = labelImage(boxList5, image6)    
    cv2.imwrite(dstFn6, image6)     

    image7 = image.copy()
    image7.fill(255)
    image7 = labelImage(boxList5, image7)    
    cv2.imwrite(dstFn7, image7)         

    #
    # Handle --process
    #

    if cfg['p']:

        #
        # Save images.
        #

        cv2.imwrite(dstFn1, image1)

        boxList = [region.bbox for region in skimage.measure.regionprops(label_image)]
        image3 = labelImage(boxList, image)
        cv2.imwrite(dstFn3, image3)   

        image4 = labelImage(boxList4, image)
        cv2.imwrite(dstFn4, image4) 
        
        #
        # Display.
        #

        fontSize = 10


        fig, axes = plt.subplots(
                      ncols=3, 
                      nrows=2)

        ax0, ax1, ax2, ax3, ax4, ax5  = axes.flat

        #
        # ax0 - Origin
        #

        ax0.imshow(image)
        ax0.set_title('Origin', fontsize=fontSize)
        ax0.axis('off')    

        #
        # ax1 - Gray
        #

        ax1.imshow(image1, cmap=plt.cm.gray)
        ax1.set_title('Gray', fontsize=fontSize)
        ax1.axis('off')

        #
        # ax2 - Edges
        #    

        ax2.imshow(edges, cmap=plt.cm.gray)
        ax2.set_title('Edges', fontsize=fontSize)
        ax2.axis('off')      
            
        #
        # ax3 - Label Items
        #        

        ax3.imshow(image3)
        ax3.set_title('Labeled Items', fontsize=fontSize)
        ax3.axis('off')            

        #
        # ax4 - Labeled Items Filtered
        #

        ax4.imshow(image4)
        ax4.set_title('Labeled Items Filtered', fontsize=fontSize)
        ax4.axis('off')  

        #
        # ax5 - Labeld Items Merged
        #

        ax5.imshow(image5)
        ax5.set_title('Labeled Items Merged', fontsize=fontSize)
        ax5.axis('off')
    
        plt.savefig(processFn)    
    

    if cfg['s']:

        plt.show()


if __name__ == '__main__':
  main()