'''
Author: Thomas Beucher

Module: TrajectoriesGenerator

Description: 
'''
import numpy as np
from Utils.ThetaNormalization import unNormNP


class TrajectoriesGenerator:
    
    def __init__(self):
        self.name = "TrajectoriesGenerator"
        self.call = 0
        self.saveCost = []
        
    def initParametersTGS(self, rs, numberOfRepeat, tg, dimState, dimOutput, mac):
        self.rs = rs
        self.numberOfRepeat = numberOfRepeat
        self.tg = tg
        self.dimState = dimState
        self.dimOutput = dimOutput
        self.mac = mac
        self.posIni = np.loadtxt(self.rs.pathFolderData + self.rs.experimentFilePosIni)
    
    def runTrajectories(self):
        pass
    
    def initTheta(self, theta):
        theta = np.asarray(theta).reshape((self.rs.numfeats**self.dimState, self.dimOutput))
        self.theta = unNormNP(theta, self.rs)
        self.mac.setThetaMAC(self.theta)
    
    def runTrajectoriesCMAWithoutParallelization(self, theta):
        self.initTheta(theta)
        costAll = [[self.tg.runTrajectory(xy[0], xy[1]) for xy in self.posIni] for i in range(self.numberOfRepeat)]
        meanByTraj = np.mean(np.asarray(costAll).reshape((self.numberOfRepeat, len(self.posIni))), axis = 0)    
        meanAll = np.mean(meanByTraj)
        self.saveCost.append(meanAll)
        print("Call n°: ", self.call, "\nCost: ", meanAll)
        self.call += 1
        return meanAll*(-1)
    
    def runTrajectoriesCMAWithParallelization(self, theta):
        pass
    
    
    
    
    