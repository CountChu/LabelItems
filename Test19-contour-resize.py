#
# https://pythontips.com/2015/03/11/a-guide-to-finding-books-in-images-using-python-and-opencv/
#

#
# import the necessary packages
#

import numpy as np
import cv2
import matplotlib.pyplot as plt
import Util

def main():

    #
    # load the image, convert it to grayscale, and blur it
    #

    #fn = "books2.jpg"
    fn = "IMG_4870.jpg"
    #fn = "IMG_4871.jpg"    
    #fn = "IMG_4889.jpg"
    image = cv2.imread(fn)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR to RGB for right color.

    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    grayImage = cv2.GaussianBlur(grayImage, (3, 3), 0)

    #
    # detect edges in the image
    #

    edgedImage = cv2.Canny(grayImage, 10, 250)
    #edgedImage = cv2.Canny(grayImage, 10, 20)

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
    
    blackImage = image.copy()
    blackImage.fill(0)
    
    whiteImage = image.copy()
    whiteImage.fill(255)
    
    for c in cnts:
    
        print ("c = %s" % c)
        
        #
        # Resize contour
        #
        
        c = Util.resizeContour(c, 1.2, finalImage)
     
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
            cv2.drawContours(finalImage, [approx], -1, (0, 255, 0), 4)
            cv2.drawContours(blackImage, [approx], -1, (0, 255, 0), 4)
            cv2.drawContours(whiteImage, [approx], -1, (0, 255, 0), 4)
            total += 1
            
    #    
    # display the output
    #

    print ("I found {0} books in that finalImage".format(total))
    
    #
    # Save finalImage, blackImage, whiteImage
    #
    
    cv2.imwrite('finalImage.jpg', finalImage) 
    cv2.imwrite('blackImage.jpg', blackImage)    
    cv2.imwrite('whiteImage.jpg', whiteImage) 

    #
    # Display image, edgedImage, closedImage, finalImage, blackImage, whiteImage
    #


    fig, axes = plt.subplots(
                  ncols=3, 
                  nrows=2,
                  figsize=(10, 6))

    ax0, ax1, ax2, ax3, ax4, ax5 = axes.flat

    fontSize = 10

    ax0.imshow(image)
    ax0.set_title('Origin', fontsize=fontSize)
    ax0.axis('off')  

    ax1.imshow(edgedImage)
    ax1.set_title('Edged', fontsize=fontSize)
    ax1.axis('off')

    ax2.imshow(closedImage)
    ax2.set_title('Closed', fontsize=fontSize)
    ax2.axis('off')
            
    ax3.imshow(finalImage)
    ax3.set_title('Final', fontsize=fontSize)
    ax3.axis('off') 

    ax4.imshow(blackImage)
    ax4.set_title('Black', fontsize=fontSize)
    ax4.axis('off')   

    ax5.imshow(whiteImage)
    ax5.set_title('White', fontsize=fontSize)
    ax5.axis('off')     

    plt.show()

if __name__ == '__main__':
    main()
