#
# http://docs.opencv.org/3.2.0/d7/d4d/tutorial_py_thresholding.html
#

import cv2
import numpy as np
from matplotlib import pyplot as plt

def main():

	img = cv2.imread('sudoku.jpg')
	rows,cols,ch = img.shape
    pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(300,300))

    fig, axes = plt.subplots(
                    ncols=3,
                    nrows=1)
    ax0, ax1, ax2 = axes.flat

    #
    # ax0 - Input
    #

    ax0.imshow(img)
    ax0.set_title('Input')

    #
    # ax1 - Process
    #

    processedImage = img.copy()
    
    for pt in pts1:
        ax1.scatter(pt[0], pt[1])

    ax1.set_prop_cycle(None)
    for pt in pts2:
        ax1.scatter(pt[0], pt[1])

    ax1.imshow(processedImage)
    ax1.set_title('Process')

    #
    # ax2 - Output
    #

    ax2.imshow(dst)
    ax2.set_title('Output')

    plt.show()

if __name__ == '__main__':
    main()    