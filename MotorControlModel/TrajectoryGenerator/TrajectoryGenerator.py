#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: Class to generate a trajectory
'''

import numpy as np

from Utils.CreateVectorUtil import createVector
from ArmModel.Arm import Arm, createStateVector, getDotQAndQFromStateVector

class TrajectoryGenerator:
    
    def __init__(self, arm, rs, cc, sizeOfTarget, Ukf, saveA, controller):
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
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.mac = arm.mac
        self.saveA = saveA
        self.controller = controller
        #Initializes variables used to save trajectory
        self.initSaveVariables()
 
    def initSaveVariables(self):
        '''
        Initializes variables used to save trajectory
        '''
        self.saveNumberOfIteration = {}
        self.saveCoordEndTraj = {}
        self.saveMvtCost = {}
        self.saveSpeed = {}
        self.saveU = {}
        self.elbowAllCoord = {}
        self.handAllCoord = {}

    def checkingKeyLoopData(self):
        '''
        Checks if the trajectory has already been run, if no, initializes the container to save it
        '''
        pass
    
    def initSaveLoopData(self):
        self.speedList = []
        self.UList = []
        self.elbowCoord = []
        self.handCoord = []
        
    def saveLoopData(self, speed, U, coordElbow, coordHand):
        '''
        Saves data generated during the trajectory

        Input:	-speed: the speed of the end effector along the trajectory, float
        '''
        self.speedList.append(speed)
        self.UList.append(U)
        self.elbowCoord.append(coordElbow)
        self.handCoord.append(coordHand)
        
    def checkingKeyEndData(self):
        '''
        Checks if the trajectory has already been run, if no, initializes the container to save it
        '''
        if not self.nameToSaveTraj in self.saveNumberOfIteration:
            self.saveNumberOfIteration[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveCoordEndTraj:
            self.saveCoordEndTraj[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveMvtCost:
            self.saveMvtCost[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveSpeed:
            self.saveSpeed[self.nameToSaveTraj] = []
        if not self.nameToSaveTraj in self.saveU:
            self.saveU[self.nameToSaveTraj] = []
        
    def saveEndData(self, nbIte, lastCoord, cost):
        '''
        Saves data generated at the end of the trajectory

        Input:	-nbIte: number of iteration ie number of time steps to finish the trajectory, int
		-lastCoord: coordinates of the end effector at the end of the trajectory, tuple
		-cost, cost of the trajectory without the reward, float
        '''
        self.checkingKeyEndData()
        self.saveNumberOfIteration[self.nameToSaveTraj].append(nbIte)
        self.saveCoordEndTraj[self.nameToSaveTraj].append(lastCoord)
        self.saveMvtCost[self.nameToSaveTraj].append(cost)
        self.saveSpeed[self.nameToSaveTraj].append(self.speedList)
        self.saveU[self.nameToSaveTraj].append(self.UList)
        self.elbowAllCoord[self.nameToSaveTraj] = self.elbowCoord
        self.handAllCoord[self.nameToSaveTraj] = self.handCoord
    
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
         #code to save data of the trajectory
        self.nameToSaveTraj = str(x) + "//" + str(y)
        if self.saveA == True:
            self.initSaveLoopData()
        #loop to generate next position until the target is reached 
        estimState = state
        while coordHand[1] < self.rs.targetOrdinate:
            #stop condition to avoid infinite loop
            if i < self.rs.numMaxIter:
                #computation of the next muscular activation vector
            #computes the next muscular activation vector using the controller theta
                U = self.controller.computeOutput(estimState, self.mac.theta)
                Ucontrol = self.mac.getNoisyCommand(U,self.rs.knoiseU)
                #computation of the arm state
                realState = self.arm.computeNextState(Ucontrol,self.arm.state)
                self.arm.setState(realState)

                #computation of the approximated state
                estimState = self.Ukf.runUKF(Ucontrol, realState)
                #computation of the cost
                cost = self.cc.computeStateTransitionCost(cost, Ucontrol, t)
                #get dotq and q from the state vector
                dotq, q = getDotQAndQFromStateVector(realState)
                #computation of the coordinates to check if the target is reach or not
                coordElbow, coordHand = self.arm.mgd(q)
                #code to save data of the trajectory
                if self.saveA == True:
                    self.saveLoopData(np.linalg.norm(dotq), Ucontrol, coordElbow, coordHand)
            else:
                break
            i += 1
            t += self.rs.dt
        #code to save data of the trajectory
        if self.saveA == True:
            self.saveEndData(i, coordHand, cost)
        #check if the target is reached and give the reward if yes
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        #return the cost of the trajectory
        return cost
    
    
    
    
    
