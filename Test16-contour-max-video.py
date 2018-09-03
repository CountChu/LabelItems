import cv2
import time
import LabelImageCv2

def main():
    
    fn = 'projector.avi'
    cam = cv2.VideoCapture(fn)

    labelImage = LabelImageCv2.LabelImage(True)

    #   
    # loop over the frames of the video
    #

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
                
        labelImage.processImages = []
        labelImage.getMaxApprox(frame)
        labeledImage = labelImage.getProcessImage('2 Before Original')
        if labeledImage is not None:
            cv2.imshow("2 Before Original", labeledImage)
                
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
