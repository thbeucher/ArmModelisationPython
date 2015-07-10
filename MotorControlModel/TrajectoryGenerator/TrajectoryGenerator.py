#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: Class to generate a trajectory
'''

from Utils.StateVectorUtil import getDotQAndQFromStateVectorS, createStateVector
from ArmModel.GeometricModel import mgd, mgi
from Utils.CreateVectorUtil import createVector
import numpy as np


class TrajectoryGenerator:
    
    def __init__(self):
        self.name = "TrajectoryGenerator"
        #Initializes variables used to save trajectory
        self.initSaveVariables()
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac):
        '''
    	Initializes the parameters used to run the functions below
    
    	Inputs:		-armP, armParameters, class object
    			-rs, readSetup, class object
    			-nsc, nextStateComputation, class object
    			-cc, costComputation, class object
    			-sizeOfTarget, size of the target, float
    			-Ukf, unscented kalaman filter, class object
    			-armD, armDynamics, class object
    			-mac, muscularActivationCommand, class object
    	'''
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        self.mac = mac

    def initSaveVariables(self):
        '''
        Initializes variables used to save trajectory
        '''
        self.saveNumberOfIteration = {}
        self.saveCoordEndTraj = {}
        self.saveMvtCost = {}
        self.saveSpeed = {}
        self.saveU = {}

    def checkingKeyLoopData(self):
        '''
        Checks if the trajectory already has been run, if no, initializes the container to save it
        '''
        if not self.nameToSaveTraj in self.saveSpeed:
            self.saveSpeed[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveU:
            self.saveU[self.nameToSaveTraj] = []
        
    def saveLoopData(self, speed, U):
        '''
        Saves data generated during the trajectory

        Input:	-speed:the speed of the end effector along the trajectory, float
        '''
        self.checkingKeyLoopData()
        self.saveSpeed[self.nameToSaveTraj].append(speed)
        self.saveU[self.nameToSaveTraj].append(U)
        
    def checkingKeyEndData(self):
        '''
        Checks if the trajectory already has been run, if no, initializes the container to save it
        '''
        if not self.nameToSaveTraj in self.saveNumberOfIteration:
            self.saveNumberOfIteration[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveCoordEndTraj:
            self.saveCoordEndTraj[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveMvtCost:
            self.saveMvtCost[self.nameToSaveTraj] = []
        
    def saveEndData(self, nbIte, lastCoord, cost):
        '''
        Saves data generated at the end of the trajectory

        Input:	-nbIte:number of iteration ie number of time steps to finish the trajectory, int
		-lastCoord:coordinate of the end effector at the end of the trajectory, tuple
		-cost, cost of the trajectory without the reward, float
        '''
        self.checkingKeyEndData()
        self.saveNumberOfIteration[self.nameToSaveTraj].append(nbIte)
        self.saveCoordEndTraj[self.nameToSaveTraj].append(lastCoord)
        self.saveMvtCost[self.nameToSaveTraj].append(cost)
    
    def runTrajectory(self, x, y):
        '''
    	Generates trajectory from the initiale position (x, y)
    
    	Inputs:		-x: absciss of the initiale position, float
    			-y: ordinate of the initiale position, float
    
    	Output:		-cost: the cost of the trajectory, float
    	'''
        #computation of the articular position q1, q2 from the initiale coordinates (x, y)
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        #create the position vector [q1, q2]
        q = createVector(q1, q2)
        #create the speed vector [dotq1, dotq2]
        dotq = createVector(0., 0.)
        #create the state vector [dotq1, dotq2, q1, q2]
        state = createStateVector(dotq, q)
        #compute the coordinates of the hand and the elbow from the position vector
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        #initializes parameters for the trajectory
        i, t, cost = 0, 0, 0
        self.Ukf.initObsStore(state)
        self.armD.initStateAD(state)
        #code to save data of the trajectory
        self.nameToSaveTraj = str(x) + "//" + str(y)
        #loop to generate next position until the target is reached 
        while coordHand[1] < self.rs.targetOrdinate:
            #stop condition to avoid infinite loop
            if i < self.rs.numMaxIter:
                #computation of the next muscular activation vector
                Ucontrol = self.mac.getCommandMAC(state)
                #computation of the arm state
                realState = self.armD.mddAD(Ucontrol)
                #computation of the approximated state
                state = self.Ukf.runUKF(Ucontrol, realState)
                #computation of the cost
                cost = self.cc.computeStateTransitionCost(cost, Ucontrol, t)
                #get dotq and q from the state vector
                dotq, q = getDotQAndQFromStateVectorS(state)
                #computation of the coordinates to check if the target is reach or not
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
                #code to save data of the trajectory
                self.saveLoopData(np.linalg.norm(dotq), Ucontrol)
            else:
                break
            i += 1
            t += self.rs.dt
        #code to save data of the trajectory
        self.saveEndData(i, coordHand, cost)
        #check if the target is reach and give the reward if yes
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        #return the cost of the trajectory
        return cost
    
    
    
    
    
