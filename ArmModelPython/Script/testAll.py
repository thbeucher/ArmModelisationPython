'''
Author: Thomas Beucher

Module: testAll

Description: 
'''
from ArmModel.GeometricModel import mgi, mgd
from Utils.CreateVectorUtil import createVector
from Utils.GenerateTrajectoryUtils import createStateVector


class TrajectoryGenerator:
    
    def __init__(self):
        self.name = "TrajectoryGenerator"
        
    def initParametersTG(self, armP, rs):
        self.armP = armP
        self.rs = rs
    
    def runTrajectory(self, x, y):
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = createVector(q1, q2)
        dotq = createVector(0., 0.)
        state = createStateVector(dotq, q)
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        i, t, cost = 0, 0, 0
        while coordHand[1] <= self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                pass
            i += 1
            

class NextStateComputation:
    
    def __init__(self):
        self.name = "NextStateComputation"
        
        
        
        
        