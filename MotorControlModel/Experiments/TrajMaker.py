#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Olivier Sigaud

Module: TrajMaker

Description: Class to generate a trajectory
'''
import numpy as np

from Utils.CreateVectorUtil import createVector
from ArmModel.Arm import Arm, createStateVector, getDotQAndQFromStateVector

from CostComputation import CostComputation
from UnscentedKalmanFilterControl import UnscentedKalmanFilterControl

class TrajMaker:
    
    def __init__(self, arm, rs, sizeOfTarget, saveA, controller):
        '''
    	Initializes the parameters used to run the functions below
    
    	Inputs:		
    			-arm, armModel, class object
                        -rs, readSetup, class object
    			-cc, costComputation, class object
    			-sizeOfTarget, size of the target, float
    			-Ukf, unscented kalman filter, class object
    			-saveA, Boolean: true = Data are saved, false = data are not saved
    	'''
        self.name = "TrajectoryGenerator"
        self.arm = arm
        self.rs = rs
        self.cc = CostComputation(rs)
        self.sizeOfTarget = sizeOfTarget
        #6 is the dimension of the state for the filter, 4 is the dimension of the observation for the filter, 25 is the delay used
        self.Ukf = UnscentedKalmanFilterControl(rs.dimStateUKF, rs.dimObsUKF, rs.delayUKF, arm, rs.knoiseU, controller)
        self.mac = arm.mac
        self.saveA = saveA
        self.controller = controller
        #Initializes variables used to save trajectory
        self.dataStore = []
        self.costStore = []
    
    def runTrajectory(self, x, y):
        '''
    	Generates trajectory from the initial position (x, y)
    
    	Inputs:		-x: abscissa of the initial position, float
    			-y: ordinate of the initial position, float
    
    	Output:		-cost: the cost of the trajectory, float
    	'''
        #computes the articular position q1, q2 from the initial coordinates (x, y)
        q1, q2 = self.arm.mgi(x, y)
        #creates the position vector [q1, q2]
        q = createVector(q1, q2)
        #creates the speed vector [dotq1, dotq2]
        dotq = createVector(0., 0.)
        #creates the state vector [dotq1, dotq2, q1, q2]
        state = createStateVector(dotq, q)

        #computes the coordinates of the hand and the elbow from the position vector
        coordElbow, coordHand = self.arm.mgd(q)
        #initializes parameters for the trajectory
        i, t, cost = 0, 0, 0
        self.Ukf.initObsStore(state)
        self.arm.setState(state)
        estimState = state
        #loop to generate next position until the target is reached 
        while coordHand[1] < self.rs.targetOrdinate and i < self.rs.numMaxIter:
            stepStore = []
            #computation of the next muscular activation vector using the controller theta
            U = self.controller.computeOutput(estimState, self.mac.theta)
            Unoisy = self.mac.getNoisyCommand(U,self.rs.knoiseU)
            #computation of the arm state
            realNextState = self.arm.computeNextState(Unoisy,self.arm.state)
            self.arm.setState(realNextState)

            #computation of the approximated state
            estimNextState = self.Ukf.runUKF(Unoisy, realNextState)
            #computation of the cost
            cost = self.cc.computeStateTransitionCost(cost, Unoisy, t)
            #get dotq and q from the state vector
            dotq, q = getDotQAndQFromStateVector(realNextState)
            #computation of the coordinates to check if the target is reach or not
            coordElbow, coordHand = self.arm.mgd(q)
            #code to save data of the trajectory

            if self.saveA == True:
                stepStore.append([0.0, self.rs.targetOrdinate])
                stepStore.append(estimState)
                stepStore.append(state)
                stepStore.append(Unoisy)
                stepStore.append(U)
                stepStore.append(estimNextState)
                stepStore.append(realNextState)
                stepStore.append(coordElbow)
                stepStore.append(coordHand)
                #print stepStore

            estimState = estimNextState
            i += 1
            t += self.rs.dt

        #check if the target is reached and give the reward if yes
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        #return the cost of the trajectory
        self.dataStore.append(stepStore)
        self.costStore.append(cost)
        return cost
    
    def saveData(self,filename):
        np.savetxt(filename+".log",self.dataStore)
        np.savetxt(filename+".cost",self.costStore)
    
    
    
