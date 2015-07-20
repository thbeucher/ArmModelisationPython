#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: Class to generate a trajectory
'''
import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

from StateVectorUtil import getDotQAndQFromStateVectorS, createStateVector
from GeometricModel import mgd, mgi
from CreateVectorUtil import createVector


cdef class TrajectoryGenerator:

    cdef:
        str name
        object armP
        object rs
        object nsc
        object cc
        public double sizeOfTarget
        object Ukf
        object armD
        object mac
        public bint saveA
        public dict saveNumberOfIteration
        public dict saveCoordEndTraj
        public dict saveMvtCost
        public dict saveSpeed
        public dict saveU
        public dict elbowAllCoord
        public dict handAllCoord
        list speedList
        list UList
        list elbowCoord
        list handCoord
        str nameToSaveTraj
        
    def __init__(self):
        self.name = "TrajectoryGenerator"
        #Initializes variables used to save trajectory
        self.initSaveVariables()
        
    cpdef initParametersTG(self, object armP, object rs, object nsc, object cc, double sizeOfTarget, object Ukf, object armD, object mac, bint saveA):
        '''
    	Initializes the parameters used to run the functions below
    
    	Inputs:		-armP, armParameters, class object
    			-rs, readSetup, class object
    			-nsc, nextStateComputation, class object
    			-cc, costComputation, class object
    			-sizeOfTarget, size of the target, float
    			-Ukf, unscented kalman filter, class object
    			-armD, armDynamics, class object
    			-mac, muscularActivationCommand, class object
    			-saveA, Boolean, true = Data are saved, false = data are not saved
    	'''
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        self.mac = mac
        self.saveA = saveA

    cpdef initSaveVariables(self):
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

    cpdef checkingKeyLoopData(self):
        '''
        Checks if the trajectory already has been run, if no, initializes the container to save it
        '''
        pass
    
    cpdef initSaveLoopData(self):
        self.speedList = []
        self.UList = []
        self.elbowCoord = []
        self.handCoord = []
        
    cpdef saveLoopData(self, double speed, np.ndarray[DTYPE_t, ndim=2] U, tuple coordElbow, tuple coordHand):
        '''
        Saves data generated during the trajectory

        Input:	-speed:the speed of the end effector along the trajectory, float
        '''
        self.speedList.append(speed)
        self.UList.append(U)
        self.elbowCoord.append(coordElbow)
        self.handCoord.append(coordHand)
        
    cpdef checkingKeyEndData(self):
        '''
        Checks if the trajectory already has been run, if no, initializes the container to save it
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
        
    cpdef saveEndData(self, int nbIte, tuple lastCoord, double cost):
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
        self.saveSpeed[self.nameToSaveTraj].append(self.speedList)
        self.saveU[self.nameToSaveTraj].append(self.UList)
        self.elbowAllCoord[self.nameToSaveTraj] = self.elbowCoord
        self.handAllCoord[self.nameToSaveTraj] = self.handCoord
    
    cpdef double runTrajectory(self, double x, double y):
        '''
    	Generates trajectory from the initiale position (x, y)
    
    	Inputs:		-x: absciss of the initiale position, float
    			-y: ordinate of the initiale position, float
    
    	Output:		-cost: the cost of the trajectory, float
    	'''
        cdef:
            double q1
            double q2
            np.ndarray[DTYPE_t, ndim=2] q
            np.ndarray[DTYPE_t, ndim=2] dotq
            np.ndarray[DTYPE_t, ndim=2] state
            tuple coordElbow
            tuple coordHand
            int i
            double t
            double cost
            np.ndarray[DTYPE_t, ndim=2] estimateState
            np.ndarray[DTYPE_t, ndim=2] Ucontrol
            np.ndarray[DTYPE_t, ndim=2] realState
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
        self.nsc.initStateNSC(state)
        #code to save data of the trajectory
        self.nameToSaveTraj = str(x) + "//" + str(y)
        if self.saveA == True:
            self.initSaveLoopData()
        #loop to generate next position until the target is reached 
        estimateState = state
        while coordHand[1] < self.rs.targetOrdinate:
            #stop condition to avoid infinite loop
            if i < self.rs.numMaxIter:
                #computation of the next muscular activation vector
                Ucontrol = self.mac.getCommandMAC(estimateState)
                #computation of the arm state
                #realState = self.armD.mddAD(Ucontrol)
                realState = self.nsc.computeNextState(Ucontrol)
                #computation of the approximated state
                estimateState = self.Ukf.runUKF(Ucontrol, realState)
                #computation of the cost
                cost = self.cc.computeStateTransitionCost(cost, Ucontrol, t)
                #get dotq and q from the state vector
                dotq, q = getDotQAndQFromStateVectorS(realState)
                #computation of the coordinates to check if the target is reach or not
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
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
        #check if the target is reach and give the reward if yes
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        #return the cost of the trajectory
        return cost
    
    
    
    
    
