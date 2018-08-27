#
# https://pythontips.com/2015/03/11/a-guide-to-finding-books-in-images-using-python-and-opencv/
#

#
# import the necessary packages
#

import numpy as np
import cv2
import matplotlib.pyplot as plt

def main():

    #
    # load the image, convert it to grayscale, and blur it
    #

    image = cv2.imread("books.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.

    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    grayImage = cv2.GaussianBlur(grayImage, (3, 3), 0)

    #
    # detect edges in the image
    #

    edgedImage = cv2.Canny(grayImage, 10, 250)

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

    finalImage = image.copy()
    for c in cnts:
     
        #
        # approximate the contour
        #
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        #
        # if the approximated contour has four points, then assume that the
        # contour is a book -- a book is a rectangle and thus has four vertices
        #
        
        if len(approx) == 4:
            cv2.drawContours(finalImage, [approx], -1, (0, 255, 0), 4)
            total += 1
            
    #    
    # display the output
    #

    print ("I found {0} books in that finalImage".format(total))

    #
    # Display image, grayImage, edgedImage, closedImage, finalImage
    #


    fig, axes = plt.subplots(
                  ncols=3, 
                  nrows=2,
                  figsize=(10, 6))

    ax0, ax1, ax2, ax3, ax4, _ = axes.flat

    fontSize = 10

    ax0.imshow(image)
    ax0.set_title('Origin', fontsize=fontSize)
    ax0.axis('off')  

    ax1.imshow(grayImage)               # the image dons't displays gray color.
    ax1.set_title('Gray', fontsize=fontSize)
    ax1.axis('off') 

    ax2.imshow(edgedImage)
    ax2.set_title('Edged', fontsize=fontSize)
    ax2.axis('off')

    ax3.imshow(closedImage)
    ax3.set_title('Closed', fontsize=fontSize)
    ax3.axis('off')
            
    ax4.imshow(finalImage)
    ax4.set_title('Final', fontsize=fontSize)
    ax4.axis('off')   

    plt.show()

if __name__ == '__main__':
    main()
