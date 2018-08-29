import cv2
import time
import LabelItemsCv2

def main():
    fn = 'IMG_4912.m4v'
    camera = cv2.VideoCapture(fn)

    labelItems = LabelItemsCv2.LabelItems(False)

    #   
    # loop over the frames of the video
    #

    while True:

        time.sleep(0.01)

        #
        # grab the current frame and initialize the occupied/unoccupied
        # text
        #

        (grabbed, frame) = camera.read()  


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

        labelItems.handleImage(frame, True)
        cv2.imshow("Original", frame)
        cv2.imshow("Final", labelItems.finalImage)
        cv2.imshow("Black", labelItems.blackImage)
        cv2.imshow("White", labelItems.whiteImage)

        #
        # If the 'q' key is pressed, break from the lop
        #

        if key == ord("q"):
            break

    #
    # cleanup the camera and close any open windows
    #

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
