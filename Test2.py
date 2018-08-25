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

def main():

    #
    # Load a JPG image file.
    #

    image = cv2.imread('IMG_4871.jpg')     # numpy.ndarray, ndim = 3
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # RGB to GRAY, ndim = 2

    fig, axes = plt.subplots(
                  ncols=1, 
                  nrows=4)

    ax0, ax1, ax2, ax3  = axes.flat

    ax0.imshow(image)
    ax0.set_title('Origin', fontsize=12)
    ax0.axis('off')    

    ax1.imshow(grayImage, cmap=plt.cm.gray)
    ax1.set_title('Gray', fontsize=12)
    ax1.axis('off')

    edges = canny(
              grayImage, 
              sigma=3,
              low_threshold=10,
              high_threshold=80)

    ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.set_title('Edges', fontsize=12)
    ax2.axis('off')

    label_image = label(edges)

    ax3.imshow(image)
    ax3.set_title('Labeled items', fontsize=12)
    ax3.axis('off')

    for region in regionprops(label_image):
        # Draw rectangle around segmented coins.
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle(
                (minc, minr),
                maxc - minc,
                maxr - minr,
                fill=False,
                edgecolor='red',
                linewidth=2)
        ax3.add_patch(rect)     
    
    #plt.tight_layout()
    plt.show()

if __name__ == '__main__':
  main()