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

    fn = "Frame2.png"
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
            thin = 5
            cv2.drawContours(finalImage, [approx], -1, (0, 255, 0), thin)
            total += 1
            
    print ("maxApprox = %s, maxAreaSize = %d" % (maxApprox, maxAreaSize))
    thin = 20    
    cv2.drawContours(finalImage, [maxApprox], -1, (0, 255, 0), thin)
    
    #
    # Perspective transform.
    #
    
    pts1 = np.float32([maxApprox[0], maxApprox[1], maxApprox[2], maxApprox[3]])
    pts2 = np.float32([
            [300,0],
            [0,0],
            [0,300],
            [300,300]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    transformedImage = cv2.warpPerspective(image, M, (300, 300))
            
    #    
    # display the output
    #

    print ("I found {0} books in that finalImage".format(total))
    
    #
    # Save finalImage
    #
    
    cv2.imwrite('finalImage.jpg', finalImage) 

    #
    # Display image, edgedImage, closedImage, finalImage, transformedImage
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
    
    ax4.imshow(transformedImage)
    ax4.set_title('Transform', fontsize=fontSize)
    ax4.axis('off')     

    ax5.axis('off')

    plt.show()

if __name__ == '__main__':
    main()
