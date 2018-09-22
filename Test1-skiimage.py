#
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4081273/
#

from skimage import data, io, filters
import numpy as np
import matplotlib.pyplot as plt

# Label image regions.
from skimage.measure import regionprops
import matplotlib.patches as mpatches
from skimage.morphology import label

from skimage.feature import canny

def main():

    # Load a small section of the image.
    image = data.coins()[0:95, 70:370]      # numpy.ndarray, image.ndim = 2

    fig, axes = plt.subplots(
                  ncols=1, 
                  nrows=3,
                  figsize=(8, 4))

    ax0, ax1, ax2  = axes.flat

    ax0.imshow(image, cmap=plt.cm.gray)
    ax0.set_title('Origin', fontsize=12)
    ax0.axis('off')

    edges = canny(
              image, 
              sigma=3,
              low_threshold=10,
              high_threshold=80)

    ax1.imshow(edges, cmap=plt.cm.gray)
    ax1.set_title('Edges', fontsize=12)
    ax1.axis('off')

    label_image = label(edges)

    ax2.imshow(image, cmap=plt.cm.gray)
    ax2.set_title('Labeled items', fontsize=12)
    ax2.axis('off')

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
        ax2.add_patch(rect)

    #plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()