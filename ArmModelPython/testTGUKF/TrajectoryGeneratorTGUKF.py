'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: 
'''
import numpy as np
from Utils.StateVectorUtil import getDotQAndQFromStateVectorS, createStateVector
from ArmModel.GeometricModel import mgd, mgi
from Utils.CreateVectorUtil import createVector


class TrajectoryGenerator:
    
    def __init__(self):
        self.name = "TrajectoryGenerator"
        self.initSaveVariables()
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac):
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        self.mac = mac
        
    def initSaveVariables(self):
        self.saveNumberOfIteration = {}
        self.saveCoordEndTraj = {}
        self.saveMvtCost = {}
        self.saveSpeed = {}
    
    def saveDataTG(self, coordUKF, coordVerif, init = 0):
        if init == 1:
            self.SaveCoordUKF, self.SaveCoordVerif = {}, {}
            self.SaveCoordUKF[self.nameToSaveTraj] = []
            self.SaveCoordVerif[self.nameToSaveTraj] = []
        self.SaveCoordUKF[self.nameToSaveTraj].append(coordUKF)
        self.SaveCoordVerif[self.nameToSaveTraj].append(coordVerif)
        
    def checkingKeyLoopData(self):
        if not self.nameToSaveTraj in self.saveSpeed:
            self.saveSpeed[self.nameToSaveTraj] = []
        
    def saveLoopData(self, speed):
        self.checkingKeyLoopData()
        self.saveSpeed[self.nameToSaveTraj].append(speed)
        
    def checkingKeyEndData(self):
        if not self.nameToSaveTraj in self.saveNumberOfIteration:
            self.saveNumberOfIteration[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveCoordEndTraj:
            self.saveCoordEndTraj[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveMvtCost:
            self.saveMvtCost[self.nameToSaveTraj] = []
        
    def saveEndData(self, nbIte, lastCoord, cost):
        self.checkingKeyEndData()
        self.saveNumberOfIteration[self.nameToSaveTraj].append(nbIte)
        self.saveCoordEndTraj[self.nameToSaveTraj].append(lastCoord)
        self.saveMvtCost[self.nameToSaveTraj].append(cost)
    
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
        
        while coordHand[1] < self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                Ucontrol = self.mac.getCommandMAC(state)
                realState = self.armD.mddAD(Ucontrol)
                state = self.Ukf.runUKF(Ucontrol, realState)
                cost = self.cc.computeStateTransitionCost(cost, Ucontrol, t)
                dotq, q = getDotQAndQFromStateVectorS(state)
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
                
                self.saveLoopData(np.linalg.norm(dotq))
            else:
                break
            i += 1
            t += self.rs.dt
        self.saveEndData(i, coordHand, cost)
            
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        return cost
    
    
    
    
    
