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
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget, Ukf, armD):
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        
    def saveDataTG(self, coordWK, coordUKF, init = 0):
        if init == 1:
            self.SaveCoordWK, self.SaveCoordUKF = {}, {}
            self.SaveCoordWK[self.nameToSaveTraj] = []
            self.SaveCoordUKF[self.nameToSaveTraj] = []
        self.SaveCoordWK[self.nameToSaveTraj].append(coordWK)
        self.SaveCoordUKF[self.nameToSaveTraj].append(coordUKF)
    
    def runTrajectory(self, x, y):
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = createVector(q1, q2)
        dotq = createVector(0., 0.)
        state = createStateVector(dotq, q)
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        i, t, cost = 0, 0, 0
        self.Ukf.initStateStore(state)
        stateUKF = state
        
        #self.nameToSaveTraj = str(x) + "//" + str(y)
        #self.saveDataTG(coordHand, coordHand, init = 1)
        
        while coordHand[1] < self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                state, U = self.nsc.computeNextState(state)
                stateUKF = self.Ukf.runUKF(state)
                cost = self.cc.computeStateTransitionCost(cost, U, t)
                dotq, q = getDotQAndQFromStateVectorS(state)
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
                dotqUKF, qUKF = getDotQAndQFromStateVectorS(stateUKF)
                coordElbowUKF, coordHandUKF = mgd(qUKF, self.armP.l1, self.armP.l2)
                #self.saveDataTG(coordHand, coordHandUKF)
            else:
                break
            i += 1
            t = self.rs.dt
        #if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
        if coordHandUKF[0] >= -self.sizeOfTarget/2 and coordHandUKF[0] <= self.sizeOfTarget/2 and coordHandUKF[1] >= 0.6175:
            cost = self.cc.computeFinalCostReward(cost, t)
        return cost
    
    
    
    
    
