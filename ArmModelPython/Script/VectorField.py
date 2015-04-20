'''
Author: Thomas Beucher

Module: VectorField 

Description: We find here script which print the moving vector for some point of space
'''

import numpy as np
import matplotlib.pyplot as plt


def vectorField():
    #Creation of some points of SPACE
    x = np.arange(-0.1, 0.11, 0.02)
    y = np.arange(0.5, 0.61, 0.02)
    p = []
    for i in range(len(x)):
        for j in range(len(y)):
            p.append((x[i], y[j]))
    px, py = [], []
    for el in p:
        px.append(el[0])
        py.append(el[1])
    plt.figure()
    plt.scatter(px, py, c = 'b')
    plt.show()
    
    
vectorField()