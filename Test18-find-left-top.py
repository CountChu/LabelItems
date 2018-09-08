import numpy as np
import sys

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
        idxRightTop = idx0
        idxLeftBottom = idx1
    else:
        idxRightTop = idx1
        idxLeftBottom = idx0
        
    leftTop = quadrangle[idxLeftTop]
    leftBottom = quadrangle[idxLeftBottom]
    rightTop = quadrangle[idxRightTop]
    rightBottom = quadrangle[idxRightBottom]
    
    return np.array([leftTop, leftBottom, rightTop, rightBottom])
    
    

def main():

    q1 = np.array([
            [0, 0],
            [0, 4],
            [3, 4],
            [3, 0]
            ])
    print("q1 = ", q1)             
    points = getOrderedPoints(q1)
    print("points = ", points)  
    print("")
    
    q2 = np.array([
            [3, 3],
            [3, 7],
            [6, 7],
            [6, 3]
            ])
    print("q2 = ", q2)              
    points = getOrderedPoints(q2)
    print("points = ", points)   
    print("")    
    
    q2 = np.array([
            [205, 186],
            [196, 309],
            [408, 310],
            [403, 184]
            ])
    print("q2 = ", q2)              
    points = getOrderedPoints(q2)
    print("points = ", points)   
    print("")     

if __name__ == '__main__':
    main()     