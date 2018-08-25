#
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4081273/
#

import cv2
from skimage import data, io, filters
import numpy as np
import matplotlib.pyplot as plt

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
                print ("%d, %d" % (i, j))
                [box1, merged1] = boxList[i]
                [box2, merged2] = boxList[j]
                if not merged1 and not merged2:
                    if overlappedArea(box1, box2):
                        return (i, j)
    return None    

def main():

    #
    # Load a JPG image file.
    #

    image = cv2.imread('IMG_4871.jpg')     # numpy.ndarray, ndim = 3
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # RGB to GRAY, ndim = 2

    fig, axes = plt.subplots(
                  ncols=1, 
                  nrows=6)

    ax0, ax1, ax2, ax3, ax4, ax5  = axes.flat

    ax0.imshow(image)
    ax0.set_title('Origin', fontsize=12)
    ax0.axis('off')    

    ax1.imshow(grayImage, cmap=plt.cm.gray)
    ax1.set_title('Gray', fontsize=12)
    ax1.axis('off')

    '''
    edges = canny(
              grayImage, 
              sigma=2, # 3
              low_threshold=20, # 10
              high_threshold=40) # 80
    '''
    edges = canny(grayImage, sigma=2)

    ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.set_title('Edges', fontsize=12)
    ax2.axis('off')

    label_image = label(edges)          # ndarray

    #
    # ax3
    #

    ax3.imshow(image)
    ax3.set_title('Labeled items', fontsize=12)
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

    regions = []
    count = 0
    for region in regionprops(label_image):
        if region.area <= 30:
            continue
        count += 1    
        print ("region = %s, %s" % (region.area, region.bbox))
        regions.append(region)        


    #
    # ax4
    #

    ax4.imshow(image)
    ax4.set_title('Labeled items filtered', fontsize=12)
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
    # ax5
    #

    ax5.imshow(image)
    ax5.set_title('Labeled items filtered', fontsize=12)
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

    #plt.tight_layout()
    plt.show()

if __name__ == '__main__':
  main()