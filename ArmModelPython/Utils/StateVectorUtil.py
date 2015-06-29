'''
Author: Thomas Beucher

Module: StateVectorUtil

Description: We find here some functions usefull to handle the state vector
'''
import numpy as np


def createStateVector(dotq, q):
        '''
        Create the state vector s [dotq1, dotq2, q1, q2]
        
        Inputs:     -dotq: numpy array
                    -q: numpy array
        
        Outputs:    -inputQ: numpy array, the state vector
        '''
        inputQ = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
        return inputQ
    
def getDotQAndQFromStateVectorS(inputQ):
    '''
    Return dotq and q from the state vector inputQ
        
    Input:      -inputQ: numpy array, state vector
        
    Outputs:    -dotq: numpy array
                -q: numpy array
    '''
    dotq = np.array([[inputQ[0,0]], [inputQ[1,0]]])
    q = np.array([[inputQ[2,0]], [inputQ[3,0]]])
    return dotq, q