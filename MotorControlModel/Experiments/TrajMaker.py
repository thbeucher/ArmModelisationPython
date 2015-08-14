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
from ArmModel.MuscularActivation import getNoisyCommand

from Regression.functionApproximator_RBFN import fa_rbfn
from Utils.FileReading import getStateAndCommandDataFromBrent, dicToArray

from CostComputation import CostComputation
from UnscentedKalmanFilterControl import UnscentedKalmanFilterControl

from GlobalVariables import BrentTrajectoriesFolder

def initRBFNController(rs):
    '''
	Initializes the controller allowing to compute the output from the input and the vector of parameters theta
	
	Input:		-rs: ReadSetup, class object
			-fr, FileReading, class object
	'''
    #Initializes the function approximator with the number of feature used
    fa = fa_rbfn(rs.numfeats,rs.inputDim,rs.outputDim)
    #Get state and command to initializes the controller by putting the features
    state, command = getStateAndCommandDataFromBrent(BrentTrajectoriesFolder)
    #Transform data from dictionary into array
    stateAll, commandAll = dicToArray(state), dicToArray(command)

    #Set the data for training the RBFN model (actually, we don't train it here, just needed for dimensioning)
    fa.setTrainingData(stateAll, commandAll)
    #set the center and width for the features
    fa.setCentersAndWidths()
    return fa

#------------------------------------------------------------------------

class TrajMaker:
    
    def __init__(self, rs, sizeOfTarget, saveA):
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

        self.arm = Arm()
        self.arm.setDT(rs.dt)

        self.controller = initRBFNController(rs)

        self.rs = rs
        self.cc = CostComputation(rs)
        self.sizeOfTarget = sizeOfTarget
        #6 is the dimension of the state for the filter, 4 is the dimension of the observation for the filter, 25 is the delay used
        self.Ukf = UnscentedKalmanFilterControl(rs.dimStateUKF, rs.dimObsUKF, rs.delayUKF, self.arm, rs.knoiseU, self.controller)
        self.saveA = saveA
        #Initializes variables used to save trajectory
        self.costStore = []

    def setTheta(self, theta):
        self.controller.setTheta(theta)
    
    def runTrajectory(self, x, y, filename):
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
        #assert(coordHand[0]==x and coordHand[1]==y), "Erreur de MGD" does not work because of rounding effects

        #initializes parameters for the trajectory
        i, t, cost = 0, 0, 0
        self.Ukf.initObsStore(state)
        self.arm.setState(state)
        estimState = state
        dataStore = []

        #loop to generate next position until the target is reached 
        while coordHand[1] < self.rs.targetOrdinate and i < self.rs.numMaxIter:
            stepStore = []
            #computation of the next muscular activation vector using the controller theta
            U = self.controller.computeOutput(estimState, self.controller.theta)
            Unoisy = getNoisyCommand(U,self.rs.knoiseU)
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
                stepStore.append(estimState.flatten().tolist())
                stepStore.append(state.flatten().tolist())
                stepStore.append(Unoisy.flatten().tolist())
                stepStore.append(U.flatten().tolist())
                stepStore.append(estimNextState.flatten().tolist())
                stepStore.append(realNextState.flatten().tolist())
                stepStore.append([coordElbow[0][0], coordElbow[1][0]])
                stepStore.append([coordHand[0][0], coordHand[1][0]])
                print ("before",stepStore)
                store = np.array(stepStore).flatten()
                print ("store",store)
                dataStore.append(store)

            estimState = estimNextState
            i += 1
            t += self.rs.dt

        #check if the target is reached and give the reward if yes
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        #return the cost of the trajectory
        self.costStore.append([x, y])
        self.costStore.append(cost)

        if self.saveA == True:
            np.savetxt(filename,dataStore)
        return cost

        
    
    
    
