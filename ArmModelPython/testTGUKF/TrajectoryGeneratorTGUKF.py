'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: 
'''
from Utils.StateVectorUtil import getDotQAndQFromStateVectorS, createStateVector
from ArmModel.GeometricModel import mgd, mgi
from Utils.CreateVectorUtil import createVector


class TrajectoryGenerator:
    
    def __init__(self):
        self.name = "TrajectoryGenerator"
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac):
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        self.mac = mac
        
    def saveDataTG(self, coordWK, init = 0):
        if init == 1:
            self.SaveCoordWK = {}
            self.SaveCoordWK[self.nameToSaveTraj] = []
        self.SaveCoordWK[self.nameToSaveTraj].append(coordWK)
    
    def runTrajectory(self, x, y):
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = createVector(q1, q2)
        dotq = createVector(0., 0.)
        state = createStateVector(dotq, q)
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        i, t, cost = 0, 0, 0
        
        self.Ukf.initObsStore(state)
        self.armD.initStateAD(state)
        
        self.nameToSaveTraj = str(x) + "//" + str(y)
        self.saveDataTG(coordHand, init = 1)
        
        while coordHand[1] < self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                Ucontrol = self.mac.getCommandMAC(state)
                realState = self.armD.mddAD(Ucontrol)
                state = self.Ukf.runUKF(Ucontrol, realState)
                cost = self.cc.computeStateTransitionCost(cost, Ucontrol, t)
                dotq, q = getDotQAndQFromStateVectorS(state)
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
                
                self.saveDataTG(coordHand)
            else:
                break
            i += 1
            t = self.rs.dt
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        return cost
    
    
    
    
    
