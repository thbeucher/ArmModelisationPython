'''
Author: Thomas Beucher

Module: OutputSolver 

Description: We find here function which return the command vector
'''

import numpy as np
from Regression import functionApproximator_RBFN
from Utils.ReadSetupFile import ReadSetupFile

def getCommand(inputgc, theta):
    '''
    Function which return the muscular activation vector U from the position vector Q
            
    Inputs:     -inputgc: (4,1) numpy array
                -theta: 2D numpy array
        
    Outputs:    -Unoise: (6,1) numpy array, noisy muscular activation vector
    '''
    fa = functionApproximator_RBFN()
    rs = ReadSetupFile()
    U = fa.functionApproximatorOutput(inputgc, theta)
    #Noise for muscular activation
    UnoiseTmp = U*(1+np.random.normal(0,rs.knoiseU))
    for i in range(UnoiseTmp.shape[0]):
        if UnoiseTmp[i] < 0:
            UnoiseTmp[i] = 0
        elif UnoiseTmp[i] > 1:
            UnoiseTmp[i] = 1
    Unoise = np.array([UnoiseTmp]).T
    return Unoise



