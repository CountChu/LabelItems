import numpy as np
import cv2

def getNorms(quadrangle):
    norms = np.linalg.norm(quadrangle, axis=1)
    print("norms = ", norms)
    idx = norms.argmin()
    print ("idx = ", idx)
    q = quadrangle - quadrangle[idx]
    print("q = ", q)
    norms = np.linalg.norm(q, axis=1)
    print("norms = ", norms)    
    return norms
    
def getOrderedPoints(quadrangle):

    norms = getNorms(quadrangle) 
    idxLeftTop = norms.argmin()
    idxRightBottom = norms.argmax()  
    
    idxList = [0, 1, 2, 3]
    idxList.pop(idxList.index(idxLeftTop))
    idxList.pop(idxList.index(idxRightBottom))
    
    print (idxList)
    
    idx0 = idxList[0]
    idx1 = idxList[1]
    p = quadrangle[idx0]
    if p[0] < p[1]:
        idxRightTop = idx1
        idxLeftBottom = idx0
    else:
        idxRightTop = idx0
        idxLeftBottom = idx1
        
    leftTop = quadrangle[idxLeftTop]
    leftBottom = quadrangle[idxLeftBottom]
    rightTop = quadrangle[idxRightTop]
    rightBottom = quadrangle[idxRightBottom]
    
    return np.array([leftTop, leftBottom, rightTop, rightBottom])
    
def resizeContour(c, factor, image=None):

    #
    # find the center of the contour (moments() or getBoundingRect())
    #
    
    m = cv2.moments(c)
    cx = int(m['m10']/m['m00'])
    cy = int(m['m01']/m['m00'])
    print (cx, cy) 
    if image is not None:
        cv2.circle(image, (cx, cy), 1, (0, 255, 0), 8)     

    #
    # subtract it from each point in the contour
    #
    
    diff = c - [cx, cy]
    print("diff = ", diff)        
    
    #
    # multiply contour points x,y by a scale factor
    #
    
    diff = diff * factor
    diff = diff.astype(int)
    
    # add the center again to each point        
    
    c = diff + [cx, cy]
    print(c)
    
    return c