import cv2
import time
import LabelImageCv2

def main():

    #fn = 'projector.avi'    
    fn = 'IMG_5081.TRIM.OUT.MP4'
    cam = cv2.VideoCapture(fn)

    #cam = cv2.VideoCapture(0)

    labelImage = LabelImageCv2.LabelImage(True)

    #   
    # loop over the frames of the video
    #

    maxApprox = None
    while True:
    
        time.sleep(0.1)    

        #
        # Read a key.
        # 

        key = cv2.waitKey(1) & 0xFF        
        print ("key = ", key)
        
        #
        # grab the current frame and initialize the occupied/unoccupied
        # text
        #

        (grabbed, frame) = cam.read()  

        #
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        #

        if not grabbed:
            break

            #
            # If the 'q' key is pressed, break from the lop
            #

            if key == ord("q"):
                break     

        cv2.imshow("Original", frame)                
                
        if maxApprox is None:        
            labelImage.processImages = []
            maxApprox = labelImage.getMaxApprox(frame)
            
        if maxApprox is not None:    
            thin = 20 
            backgroundImage = frame.copy()
            cv2.drawContours(backgroundImage, [maxApprox], -1, (0, 255, 0), thin)
            cv2.imshow("Background", backgroundImage)
            
            transformedImage = labelImage.transform(frame, maxApprox, 640, 480)
            cv2.imshow("Transformed", transformedImage)
            
            labelImage.handle(transformedImage, False)
            cv2.imshow("Final", labelImage.finalImage)
            cv2.imshow("White", labelImage.whiteImage)
                
        '''
        labelImage.handle(frame, True)
        cv2.imshow("Final", labelImage.finalImage)
        cv2.imshow("Black", labelImage.blackImage)
        cv2.imshow("White", labelImage.whiteImage)
        '''
        
        #
        # If the 'q' key is pressed, break from the lop
        #

        if key == ord("q"):
            break
            

    #
    # cleanup the camera and close any open windows
    #

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
