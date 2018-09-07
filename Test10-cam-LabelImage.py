import cv2
import time
import LabelImageCv2

def main():
    
    #fn = 'IMG_4912.m4v'
    #cam = cv2.VideoCapture(fn)

    cam = cv2.VideoCapture(0)    

    labelImage = LabelImageCv2.LabelImage(False)

    #   
    # loop over the frames of the video
    #

    while True:

        time.sleep(0.01)

        #
        # grab the current frame and initialize the occupied/unoccupied
        # text
        #

        (grabbed, frame) = cam.read()  


        #
        # Read a key.
        # 

        key = cv2.waitKey(1) & 0xFF        

        #
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        #

        if not grabbed:

            #
            # If the 'q' key is pressed, break from the lop
            #

            if key == ord("q"):
                break     

        labelImage.handleImage(frame, True)
        cv2.imshow("Original", frame)
        cv2.imshow("Final", labelImage.finalImage)
        cv2.imshow("Black", labelImage.blackImage)
        cv2.imshow("White", labelImage.whiteImage)

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
