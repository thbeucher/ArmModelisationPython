#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: Experiments

Description: Class used to generate all the trajectories of the experimental setup and also used for CMAES optimization
'''

import time
import numpy as np
from Utils.ThetaNormalization import unNormNP
from Utils.ReadSetupFile import ReadSetupFile

from GlobalVariables import pathDataFolder

from Experiments.TrajMaker import TrajMaker

class Experiments:
    def __init__(self, arm, rs, sizeOfTarget, saveA, controller):
        '''
    	Initializes parameters used to run functions below
    
    	Inputs:
    			-numberOfRepeat: number given how many times each trajectory are run, int
    			-tm: trajMaker: class object
    			-dimState: dimension of the state, int
    			-dimOutput: dimension of the output, here the output correspond to the muscular activation vector U
    			-mac: muscularActivationCommand, class object
    	'''
        self.name = "Experiments"
        self.call = 0
        self.saveCost = []
        self.numfeats = rs.numfeats
        self.numberOfRepeat = rs.numberOfRepeatEachTraj
        self.tm = TrajMaker(arm, rs, sizeOfTarget, saveA, controller)
        self.dimState = rs.inputDim
        self.dimOutput = rs.outputDim
        self.mac = arm.mac
        self.posIni = np.loadtxt(pathDataFolder + rs.experimentFilePosIni)
    
    def initTheta(self, theta):
        '''
    	Initializes the controller (i.e. the vector of parameters) for the rest of the code used to generate trajectories
    
    	Input:		-theta: controller ie vector of parameters, numpy array
    	'''
        self.theta = np.copy(theta)
        #reshaping of the parameters vector because this function is used by the cmaes algorithm and cmaes feed the function with a one dimension numpy array but in the rest of the algorithm the 2 dimensions numpy array is expected for the vector of parameters theta
        self.theta = np.asarray(self.theta).reshape((self.numfeats**self.dimState, self.dimOutput))
        #UnNorm the vector of parameters, because for cmaes we use a normalize vector
        self.theta = unNormNP(self.theta)
        #give the theta to the muscularActivationCommand class
        self.mac.setThetaMAC(self.theta)

    def saveData(self, foldername):
        nameToSaveThetaCma = rs.CMAESpath + str(sizeOfTarget) + "/"
        i = 1
        for el in os.listdir(foldername):
            tryName = "traj" + str(i) + ".log"
            if tryName in el:
                i += 1
                tryName = "traj" + str(i) + ".log"
        filename = foldername + tryname
        tm.saveData(filename)
        
    def saveThetaCmaes(self, meanCost, iter):
        rs = ReadSetupFile()
        nameFileSave = rs.CMAESpath + str(self.tm.sizeOfTarget) + "/thetaTmp" + str(iter)
        f = open(nameFileSave, 'ab')
        np.savetxt(f, self.theta)
        nameFileSaveMeanCost = rs.CMAESpath + str(self.tm.sizeOfTarget) + "/meanCost" + str(iter)
        g = open(nameFileSaveMeanCost, 'ab')
        np.savetxt(g, np.asarray([meanCost]))
        
    def runOneTrajectory(self, theta, coord):
        thetaTG = np.copy(theta)
        self.mac.setThetaMAC(thetaTG)
        cost = self.tm.runTrajectory(coord[0], coord[1])
        return cost
        
    def runTrajectoriesResultsGeneration(self, theta, repeat, rbfn = False):
        if rbfn == False:
            self.initTheta(theta)
        else:
            thetaTG = np.copy(theta)
            self.mac.setThetaMAC(thetaTG)
        costAll = [[self.tm.runTrajectory(xy[0], xy[1]) for xy in self.posIni] for i in range(repeat)]
        meanByTraj = np.mean(np.asarray(costAll).reshape((repeat, len(self.posIni))), axis = 0)    
        return meanByTraj
    
    def runTrajectoriesCMAES(self, theta):
        '''
    	Generates all the trajectories of the experimental setup and return the mean cost. This function is used by cmaes to optimize the controller.
    
    	Input:		-theta: vector of parameters, one dimension normalized numpy array
    
    	Ouput:		-meanAll: the mean of the cost of all trajectories generated, float
    	'''
        t0 = time.time()
        self.initTheta(theta)
        #compute all the trajectories x times each, x = numberOfRepeat
        costAll = [[self.tm.runTrajectory(xy[0], xy[1]) for xy in self.posIni] for i in range(self.numberOfRepeat)]
        #compute the mean cost for the x times generated trajectories
        meanByTraj = np.mean(np.asarray(costAll).reshape((self.numberOfRepeat, len(self.posIni))), axis = 0)   
        #compute the mean cost for all trajectories 
        meanAll = np.mean(meanByTraj)
        self.saveCost.append(meanAll)
        print("Call #: ", self.call, "\n Cost: ", meanAll, "\n Time: ", time.time() - t0, "s")
        self.saveThetaCmaes(meanAll,self.call)
        self.call += 1
        return meanAll*(-1)
    
    
    
    
