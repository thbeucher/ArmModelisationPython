#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: TrajectoriesGenerator

Description: Class used to generate all the trajectories of the experimental setup and also used for the cmaes otpimization
'''

import time
import numpy as np
from Utils.ThetaNormalization import unNormNP
from GlobalVariables import pathDataFolder


class TrajectoriesGenerator:
    
    def __init__(self):
        self.name = "TrajectoriesGenerator"
        self.call = 0
        self.saveCost = []
        
    def initParametersTGS(self, rs, numberOfRepeat, tg, dimState, dimOutput, mac):
        '''
    	Initializes parameters used to run functions below
    
    	Inputs:		-rs: readSetup, class object
    			-numberOfRepeat: number given how many times each trajectory are run, int
    			-tg: trajectoryGenerator: class object
    			-dimState: dimension of the state, int
    			-dimOutput: dimension of the output, here the output correspond to the muscular activation vector U
    			-mac: muscularActivationCommand, class object
    	'''
        self.rs = rs
        self.numberOfRepeat = numberOfRepeat
        self.tg = tg
        self.dimState = dimState
        self.dimOutput = dimOutput
        self.mac = mac
        self.posIni = np.loadtxt(pathDataFolder + self.rs.experimentFilePosIni)
    
    def runTrajectories(self):
        pass
    
    def initTheta(self, theta):
        '''
    	Initializes the controller (ie the vector of parameters) for the rest of the code used to generate trajectories
    
    	Input:		-theta: controller ie vector of parameters, numpy array
    	'''
        self.theta = np.copy(theta)
        #reshaping of the parameters vector because this function is used by the cmaes algorithm and cmaes feed the function with a one dimension numpy array but in the rest of the algorithm the 2 dimensions numpy array is expected for the vector of parameters theta
        self.theta = np.asarray(self.theta).reshape((self.rs.numfeats**self.dimState, self.dimOutput))
        #UnNorm the vector of parameters, because for cmaes we use a normalize vector
        self.theta = unNormNP(self.theta, self.rs)
        #give the theta to the muscularActivationCommand class
        self.mac.setThetaMAC(self.theta)
        
    def saveThetaCmaes(self, meanCost):
        nameFileSave = pathDataFolder + "OptimisationResults/ResCma" + str(self.tg.sizeOfTarget) + "/thetaSolTmp_target" + str(self.tg.sizeOfTarget)
        f = open(nameFileSave, 'ab')
        np.savetxt(f, self.theta)
        nameFileSaveMeanCost = pathDataFolder + "OptimisationResults/ResCma" + str(self.tg.sizeOfTarget) + "/meanCost" + str(self.tg.sizeOfTarget)
        g = open(nameFileSaveMeanCost, 'ab')
        np.savetxt(g, np.asarray([meanCost]))
        
    def runTrajectoriesResultsGeneration(self, theta, repeat):
        #self.initTheta(theta)
        thetaTG = np.copy(theta)
        thetaTG = np.asarray(thetaTG).reshape((self.rs.numfeats**self.dimState, self.dimOutput))
        self.mac.setThetaMAC(thetaTG)
        costAll = [[self.tg.runTrajectory(xy[0], xy[1]) for xy in self.posIni] for i in range(repeat)]
        meanByTraj = np.mean(np.asarray(costAll).reshape((repeat, len(self.posIni))), axis = 0)    
        return meanByTraj
    
    def runTrajectoriesCMAWithoutParallelization(self, theta):
        '''
    	Generates all the trajectories of the experimental setup and return the mean cost. This function is used by cmaes to otpimize the controller.
    
    	Input:		-theta: vector of parameters, one dimension normalized numpy array
    
    	Ouput:		-meanAll: the mean of the cost of all trajectories generated, float
    	'''
        t0 = time.time()
        self.initTheta(theta)
        #compute all the trajectories x times each, x = numberOfRepeat
        costAll = [[self.tg.runTrajectory(xy[0], xy[1]) for xy in self.posIni] for i in range(self.numberOfRepeat)]
        #compute the mean cost for the x times generated trajectories
        meanByTraj = np.mean(np.asarray(costAll).reshape((self.numberOfRepeat, len(self.posIni))), axis = 0)   
        #compute the mean cost for all trajectories 
        meanAll = np.mean(meanByTraj)
        self.saveCost.append(meanAll)
        print("Call n°: ", self.call, "\nCost: ", meanAll, "\nTime: ", time.time() - t0)
        self.call += 1
        self.saveThetaCmaes(meanAll)
        return meanAll*(-1)
    
    def runTrajectoriesCMAWithParallelization(self, theta):
        pass
    
    
    
    
    
