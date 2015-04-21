'''
Author: Thomas Beucher

Module: ChangeExperimentalSetup

Description: Script to change the initial position
'''

import numpy as np
import math
import matplotlib.pyplot as plt
from Utils.FileSaving import fileSavingBin

def changeExperiment():
    x0, y0, r1, r2 = 0, 0.6175, 0.2275, 0.3575
    x, y, exper = [], [], []
    #nppi = np.arange(5*math.pi/4, 7*math.pi/4, math.pi/10)
    nppi = np.linspace(5*math.pi/4, 7*math.pi/4, 6)
    for i in range(nppi.shape[0]):
        xt1 = x0 + r1 * math.cos(nppi[i])
        yt1 = y0 + r1 * math.sin(nppi[i])
        x.append(xt1)
        y.append(yt1)
        exper.append((xt1, yt1))
        
        xt2 = x0 + r2 * math.cos(nppi[i])
        yt2 = y0 + r2 * math.sin(nppi[i])
        x.append(xt2)
        y.append(yt2)
        exper.append((xt2, yt2))
            
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.show()
    
    fileSavingBin("PosIniExperimentCircular", exper)

#changeExperiment()



