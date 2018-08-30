import cv2
import time

def main():
    #fn = 'IMG_4912.m4v'
    #camera = cv2.VideoCapture(fn)

    camera = cv2.VideoCapture(0)

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

        cv2.imshow("Security Feed", frame)


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
