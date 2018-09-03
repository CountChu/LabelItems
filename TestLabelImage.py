import sys
import os
import getopt

import math
import cv2
import matplotlib.pyplot as plt

import LabelImageSki    
import LabelImageCv2 

def help():
    print ("Usage:")
    print ("    python TestLabelImage.py IMG_4889.jpg -p -s")    
    print ("        -h, --help") 
    print ("        -p, --process")      
    print ("        -s, --show")
    print ("        -a, --algorithm")  
    print ('            a1, Cv2')
    print ('            a2, Ski')

def main():

    if len(sys.argv) <= 1:
        help()
        sys.exit(0)

    fn = sys.argv[1]

    #
    # Parse arguments.
    #

    cfg = {
        'h': False,
        's': False,
        'p': False,
        'a': 'a1'}

    try:
        (opts, args) = getopt.getopt(
            sys.argv[2:], 
            "hspa:",
            ["help", "show", "process", "algorithm"])
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(0)
        
    for o, a in opts:
        if o in ('-h', '--help'):
            cfg['h'] = True
        elif o in ('-p', '--process'):
            cfg['p'] = True
        elif o in ('-s', '--show'):
            cfg['s'] = True
        elif o in ('-a', '--algorithm'):
            cfg['a'] = a
        else:
            help()
            sys.exit(0)

    print (opts)

    if cfg['h']:
        help()
        sys.exit(0)     

    if cfg['a'] == 'a1':
        labelImage = LabelImageCv2.LabelImage(cfg['p'])           
    elif cfg['a'] == 'a2':
        labelImage = LabelImageSki.LabelImage(cfg['p'])        
    else:
        help()
        sys.exit(0)
        
    #
    # Find max contour.
    #
    
    image = cv2.imread(fn)
    maxApprox = labelImage.getMaxApprox(image)
    transformedImage = labelImage.transform(image, maxApprox)

    #
    # Label the transformed image.
    #    

    labelImage.handleImage(transformedImage, False)

    #
    # Handle --process
    #

    if cfg['p']:

        #
        # Prepare file names of output
        #
        
        (dstFn, ext) = os.path.splitext(fn);
        
        #
        # Save process images.
        #

        print ("len(processImages) = %d" % len(labelImage.processImages))
        i = 1
        for pi in labelImage.processImages:
            (title, image, canSave) = pi
            if not canSave:
                i += 1
                continue

            dstFni = dstFn + "-" + cfg['a'] + "-" + str(i) + ext
            i += 1

            print ("save ", dstFni)
            cv2.imwrite(dstFni, image)

        #
        # Handle --show
        #    

        if cfg['s']:
        
            fontSize = 10

            cols = 3
            rows = math.ceil(len(labelImage.processImages) / cols)
            fig, axes = plt.subplots(
                          ncols=cols, 
                          nrows=rows)

            print ("len(axes.flat) = ", len(axes.flat))
            for ax in axes.flat:
                ax.axis('off')

            i = 0
            for pi in labelImage.processImages:
                (title, image, canSave) = pi 
                ax = axes.flat[i]
                i += 1
                ax.imshow(image)
                ax.set_title(title, fontsize = 10)


            processFn = dstFn + "-" + cfg['a'] +  "-Process" + ext
            print ("processFn = "+processFn)            
            plt.savefig(processFn)    

            plt.show()


if __name__ == '__main__':
  main()