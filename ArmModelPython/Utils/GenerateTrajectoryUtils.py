'''
Author: Thomas Beucher

Module: GenerateTrajectoryUtils

Description: We find here some functions usefull for the class GenerateTrajectory
'''
import numpy as np
from ArmModel.ArmDynamics import mdd
from ArmModel.GeometricModel import jointStop
    
    
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
    
    
class NextState:
    
    def __init__(self, armP, musclesP, dt, theta, fa, knoiseU):
        self.name = "NextState"
        self.armP = armP
        self.musclesP = musclesP
        self.dt = dt
        self.theta = theta
        self.GC = CommandU(fa, knoiseU)
        
    def computeNextState(self, inputQ):
        '''
        Computes the next state
        
        Input:     -inputQ: numpy array (state_dimension, ), the state vector s at time t (dotq1, dotq2, q1, q2)
        
        Output:    -outputQ: numpy array (state_dimension, ), the state vector at time t+1
        '''
        dotq, q = getDotQAndQFromStateVectorS(inputQ)
        U = self.GC.getCommand(inputQ, self.theta)
        ddotq, dotq, q = mdd(q, dotq, U, self.armP, self.musclesP, self.dt)
        q = jointStop(q)
        outputQ = createStateVector(dotq, q)
        return outputQ, U
    
class CommandU:
    
    def __init__(self, fa, knoiseU):
        self.name = "Command"
        self.fa = fa
        self.knoiseU = knoiseU
        
    def getCommand(self, inputgc, theta):
        '''
        Returns the muscular activation vector U from the position vector Q
        Inputs:     -inputgc: (4,1) numpy array, vector [dotq1, dotq2, q1, q2]
                    -theta: 2D numpy array, the controler generate by rbfn
        
        Outputs:    -Unoise: (6,1) numpy array, noisy muscular activation vector
        '''
        U = self.fa.computesOutput(inputgc, theta)
        #Noise for muscular activation
        UnoiseTmp = U*(1+ np.random.normal(0,self.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    
    