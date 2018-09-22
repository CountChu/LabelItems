import numpy as np
import sys
import Util

def main():

    q1 = np.array([
            [0, 0],
            [0, 4],
            [3, 4],
            [3, 0]
            ])
    print("q1 = ", q1)             
    points = Util.getOrderedPoints(q1)
    print("points = ", points)  
    print("")
    
    q2 = np.array([
            [3, 3],
            [3, 7],
            [6, 7],
            [6, 3]
            ])
    print("q2 = ", q2)              
    points = Util.getOrderedPoints(q2)
    print("points = ", points)   
    print("")    
    
    q2 = np.array([
            [205, 186],
            [196, 309],
            [408, 310],
            [403, 184]
            ])
    print("q2 = ", q2)              
    points = Util.getOrderedPoints(q2)
    print("points = ", points)   
    print("")     

if __name__ == '__main__':
    main()     