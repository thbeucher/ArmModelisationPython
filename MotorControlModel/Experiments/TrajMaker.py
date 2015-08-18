#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Olivier Sigaud

Module: TrajMaker

Description: Class to generate a trajectory
'''
import numpy as np

from Utils.CreateVectorUtil import createVector
from ArmModel.Arm import Arm, getDotQAndQFromStateVector
from ArmModel.MuscularActivation import getNoisyCommand

from Regression.RBFN import rbfn

from Utils.FileReading import getStateAndCommandData, dicToArray

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
    fa = rbfn(rs.numfeats,rs.inputDim,rs.outputDim)
    #Get state and command to initializes the controller by putting the features
    state, command = getStateAndCommandData(BrentTrajectoriesFolder)
    #Transform data from dictionary into array
    stateAll, commandAll = dicToArray(state), dicToArray(command)

    #Set the data for training the RBFN model (actually, we don't train it here, just needed for dimensioning)
    fa.setTrainingData(stateAll, commandAll)
    #set the center and width for the features
    return fa

#------------------------------------------------------------------------

class TrajMaker:
    
    def __init__(self, rs, sizeOfTarget, saveA, thetaFile):
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
        #load the controller, i.e. the vector of parameters theta
        theta = self.controller.loadTheta(thetaFile)
        #put theta to a one dimension numpy array, ie row vector form
        #theta = matrixToVector(theta)
 
        self.rs = rs
        self.cc = CostComputation(rs)
        self.sizeOfTarget = sizeOfTarget
        #6 is the dimension of the state for the filter, 4 is the dimension of the observation for the filter, 25 is the delay used
        self.Ukf = UnscentedKalmanFilterControl(rs.dimStateUKF, rs.delayUKF, self.arm, rs.knoiseU, self.controller)
        self.saveA = saveA
        #Initializes variables used to save trajectory
 
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
        #creates the state vector [dotq1, dotq2, q1, q2]
        q = createVector(q1,q2)
        state = np.array([0., 0., q1, q2])
        #print("coord init ",[x,y])

        #computes the coordinates of the hand and the elbow from the position vector
        coordElbow, coordHand = self.arm.mgd(q)
        #assert(coordHand[0]==x and coordHand[1]==y), "Erreur de MGD" does not work because of rounding effects

        #initializes parameters for the trajectory
        i, t, cost = 0, 0, 0
        self.Ukf.initObsStore(state)
        self.arm.setState(state)
        estimState = state
        #estimState = np.array([0.2, 0.2, 0.2, 0.2])
        dataStore = []

        #loop to generate next position until the target is reached 
        while coordHand[1] < self.rs.YTarget and i < self.rs.numMaxIter:
            stepStore = []
            #computation of the next muscular activation vector using the controller theta
            #print ("state :",self.arm.state)

            U = self.controller.computeOutput(estimState)
            #U = self.controller.computeOutput(self.arm.state) #used to ignore the filter

            #print ("U:",U)
            Unoisy = getNoisyCommand(U,self.rs.knoiseU)
            #computation of the arm state
            realNextState = self.arm.computeNextState(Unoisy, self.arm.state)
 
            #computation of the approximated state
            tmpstate = self.arm.state
            estimNextState = self.Ukf.runUKF(tmpstate)
            #print estimNextState
            #estimNextState = np.array([0.2, 0.2, 0.2, 0.2,])

            self.arm.setState(realNextState)

            #computation of the cost
            cost = self.cc.computeStateTransitionCost(cost, Unoisy, t)
            #get dotq and q from the state vector
            dotq, q = getDotQAndQFromStateVector(realNextState)
            #print ("dotq :",dotq)
            #computation of the coordinates to check if the target is reach or not
            #code to save data of the trajectory

            #Note : these structures might be much improved
            if self.saveA == True:
                qt1, qt2 = self.arm.mgi(self.rs.XTarget, self.rs.YTarget)
 
                stepStore.append([0.0, 0.0, qt1, qt2])
                stepStore.append(estimState)
                stepStore.append(tmpstate)
                stepStore.append(Unoisy)
                stepStore.append(np.array(U))
                stepStore.append(estimNextState)
                stepStore.append(realNextState)
                stepStore.append([coordElbow[0], coordElbow[1]])
                stepStore.append([coordHand[0], coordHand[1]])
                #print ("before",stepStore)
                tmpstore = np.array(stepStore).flatten()
                row = [item for sub in tmpstore for item in sub]
                #print ("store",row)
                dataStore.append(row)

            estimState = estimNextState
            coordElbow, coordHand = self.arm.mgd(q)
            i += 1
            t += self.rs.dt

        #check if the target is reached and give the reward if yes
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.YTarget:
            cost = self.cc.computeFinalCostReward(cost, t)
   
        if self.saveA == True:
            np.savetxt(filename,dataStore)

        #print "end of trajectory"
        return cost, t

        
    
    
    
