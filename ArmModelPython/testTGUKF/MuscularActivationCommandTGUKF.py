'''
Author: Thomas Beucher

Module: MuscularActivationCommand

Description: 
'''
import numpy as np

class MuscularActivationCommand:
    
    def __init__(self):
        self.name = "MuscularActivationCommand"
        
    def initParametersMAC(self, fa, rs):
        self.fa = fa
        self.rs = rs
        
    def setThetaMAC(self, theta):
        self.theta = theta
    
    def getCommandMAC(self, state):
        U = self.fa.computesOutput(state, self.theta)
        UnoiseTmp = U*(1+ np.random.normal(0,self.rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    
    
    
    
