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

# Label image regions.
from skimage.measure import regionprops
import matplotlib.patches as mpatches
from skimage.morphology import label

from skimage.feature import canny

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

    labelFn = dstFn + "-Label" + ext
    print ("labelFn = "+labelFn)

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
        usage()
        sys.exit(0)
        
    for o, a in opts:
        if o in ('-h', '--help'):
            cfg['h'] = True
        elif o in ('-s', '--show'):
            cfg['s'] = True
        elif o in ('-p', '--process'):
            cfg['p'] = True
        else:
            usage()
            sys.exit(0)

    #
    # Load a JPG image file.
    #

    image = cv2.imread(fn)     # numpy.ndarray, ndim = 3
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # RGB to GRAY, ndim = 2

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

    ax1.imshow(grayImage, cmap=plt.cm.gray)
    ax1.set_title('Gray', fontsize=fontSize)
    ax1.axis('off')

    #
    # ax2 - Edges
    #

    edges = canny(
              grayImage, 
              sigma=2, # 3
              low_threshold=0, # 10
              high_threshold=15) # 80
    #edges = canny(grayImage, sigma=2)

    ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.set_title('Edges', fontsize=fontSize)
    ax2.axis('off')

    label_image = label(edges)          # ndarray

    #
    # ax3 - Label Items
    #

    ax3.imshow(image)
    ax3.set_title('Labeled Items', fontsize=fontSize)
    ax3.axis('off')

    count = 0
    for region in regionprops(label_image):

        print ("region = %s, %s" % (region.area, region.bbox))
        
        #
        # Draw rectangle around segmented objects.
        #

        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle(
                (minc, minr),
                maxc - minc,
                maxr - minr,
                fill=False,
                edgecolor='red',
                linewidth=2)
        print ("rect = %s" % rect)
        ax3.add_patch(rect)     
        count += 1
    print ("count = ", count)

    #
    # Filter regions.
    #

    maxRegionArea = 0
    for region in regionprops(label_image):
        regionArea = getArea(region.bbox)
        maxRegionArea = max(maxRegionArea, regionArea)
    print ("maxRegionArea = ", maxRegionArea)

    regions = []
    count = 0
    imageArea = image.shape[0] * image.shape[1]
    for region in regionprops(label_image):
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
        regions.append(region)        

    #
    # ax4 - Labeled Items Filtered
    #

    ax4.imshow(image)
    ax4.set_title('Labeled Items Filtered', fontsize=fontSize)
    ax4.axis('off')

    print("len(regions) = %d" % len(regions))
    for region in regions:

        #
        # Draw rectangle around segmented objects.
        #        

        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle(
                (minc, minr),
                maxc - minc,
                maxr - minr,
                fill=False,
                edgecolor='red',
                linewidth=2)
        print ("rect = %s" % rect)
        ax4.add_patch(rect) 

    #
    # Transform regions to boxList
    #     

    boxList = []
    for region in regions:
        boxList.append([region.bbox, False])

    #
    # merge overlapped boxList.
    #    

    while True:
        result = findOverlappedRegions(boxList)
        if result == None:
            break

        (i, j) = result
        [box1, merged1] = boxList[i]
        [box2, merged2] = boxList[j]
        box = mergeArea(box1, box2)
        print ("box = %s" % str(box))
        boxList[i][1] = True
        boxList[j][1] = True
        boxList.append([box, False])

    for box in boxList:
        print(box)

    #
    # ax5 - Labeld Items Merged
    #

    ax5.imshow(image)
    ax5.set_title('Labeled Items Merged', fontsize=fontSize)
    ax5.axis('off')

    for [box, merged] in boxList:
        if merged:
            continue


        #
        # Draw rectangle around segmented objects.
        #        

        (minr, minc, maxr, maxc) = box
        rect = mpatches.Rectangle(
                (minc, minr),
                maxc - minc,
                maxr - minr,
                fill=False,
                edgecolor='red',
                linewidth=2)
        print ("rect = %s" % rect)
        ax5.add_patch(rect)          

    
    if cfg['p']:
        plt.savefig(processFn)    
    

    if cfg['s']:
        plt.show()


if __name__ == '__main__':
  main()