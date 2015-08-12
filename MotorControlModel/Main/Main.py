#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: Main

Description: useful functions to run cmaes and some scripts to run trajectories
'''

import os
import cma
import numpy as np

from multiprocessing.pool import Pool

from Utils.FileReading import getStateAndCommandDataFromBrent, dicToArray
from Utils.ThetaNormalization import normalizationNP, matrixToVector, normalizationNPWithoutSaving
from Utils.FileSaving import fileSavingAllDataJson, fileSavingScattergramJson
from Utils.ReadDataTmp import getBestTheta
from Utils.ReadSetupFile import ReadSetupFile
from Utils.PurgeData import purgeCostNThetaTmp

from ArmModel.Arm import Arm

from Regression.functionApproximator_RBFN import fa_rbfn

from Kalman.UnscentedKalmanFilterControl import UnscentedKalmanFilterControl
from TrajectoryGenerator.TrajectoryGenerator import TrajectoryGenerator
from Experiments.Experiments import Experiments
from CostComputation.CostComputation import CostComputation
from GlobalVariables import BrentTrajectoriesFolder, pathDataFolder, cmaesPath

def initRBFNController(rs):
    '''
	Initializes the controller allowing to compute the output from the input and the vector of parameters theta
	
	Input:		-rs: ReadSetup, class object
			-fr, FileReading, class object
	'''
    #Initializes the function approximator with the number of feature used
    fa = fa_rbfn(rs.numfeats)
    #Get state and command to initializes the controller by putting the features
    state, command = getStateAndCommandDataFromBrent(BrentTrajectoriesFolder)
    #Transform data from dictionary into array
    stateAll, commandAll = dicToArray(state), dicToArray(command)
    #print("nombre d'echantillons state : ", len(stateAll))
    #print("nombre d'echantillons commande : ", len(commandAll))
    #print("echantillon commande : ", commandAll[0])

    #Set the data for training the RBFN model
    fa.setTrainingData(stateAll, commandAll)
    #set the center and width for the features
    fa.setCentersAndWidths()
    return fa

def initAll(sizeOfTarget, rs, save = False):
    '''
	Initializes class object needed to generate trajectories
	
	Input:		-sizeOfTarget: the size of the target, float
				-fr, FileReading, class object
				-rs, ReadSetup, class object
	'''
    #fa, function approximator ie the controller
    fa = initRBFNController(rs)
    #arm model
    arm = Arm()
    arm.setDT(rs.dt)
    #ukf, unscented kalman filter
    #6 is the dimension of the state for the filter, 4 is the dimension of the observation for the filter, 25 is the delay used
    Ukf = UnscentedKalmanFilterControl(rs.dimStateUKF, rs.dimObsUKF, rs.delayUKF, arm, rs.knoiseU, fa)
    #cc, cost computation
    cc = CostComputation(rs)
    #tg, trajectory generator
    tg = TrajectoryGenerator(arm, rs, cc, sizeOfTarget, Ukf, save, fa)
    #here 5 is the number of repeat of each trajectory, 4 is the dimension of the input, 6 is the dimension of the ouput
    exp = Experiments(rs.numfeats, rs.numberOfRepeatEachTraj, tg, rs.inputDim, rs.outputDim, arm.mac, rs.experimentFilePosIni)
    return exp

def generateTrajectoryForScattergram(nameFolderSave, repeat, nameT = 'None'):
    rs = ReadSetupFile()
    for el in rs.sizeOfTarget:
        thetaName = pathDataFolder + "cmaesPath/ResCma" + str(el) + "/thetaCma" + str(el) + "TGUKF" + str(nameT)
        theta = np.loadtxt(thetaName)
        tgs = initAll(el, rs, True)
        cost = tgs.runTrajectoriesResultsGeneration(theta, repeat)
        print("Cost: ", cost)
        fileSavingScattergramJson(el, tgs.tg, nameFolderSave)
        print("End of generation")

def generateTrajectoryRBFN(nameFolder, nameT = 'None'):
    rs = ReadSetupFile()
    if nameT == 'None':
        thetaName = pathDataFolder + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    else:
        thetaName = pathDataFolder + "RBFN2/" + str(rs.numfeats) + "feats/" + nameT
    theta = np.loadtxt(thetaName)
    print("Enter coordinate of the initial point!")
    x = input("x: ")
    x = float(x)
    y = input("y: ")
    y = float(y)
    coord = (x, y)
    tgs = initAll(rs.sizeOfTarget[3], rs, True)
    cost = tgs.runOneTrajectoryRBFN(theta, coord)
    print("Cost: ", cost)
    fileSavingAllDataJson(0, tgs.tg, nameFolder, True)
    print("End of generation")
    
def generateResultsRBFN(nbret, nameT):
    rs = ReadSetupFile()
    pathName = pathDataFolder + "RBFN2/" + str(rs.numfeats) + "feats/" 
    thetaName = pathName + nameT
    theta = np.loadtxt(thetaName)
    tgs = initAll(rs.sizeOfTarget[3], rs, True)
    cost = tgs.runTrajectoriesResultsGeneration(theta, nbret, True)
    print("Cost: ", cost)
    fileSavingAllDataJson(0, tgs.tg, pathName, True)
    print("End of generation")
    
    
def generateResults(nameFolderSave, nbret, nameT):
    rs = ReadSetupFile()
    for el in rs.sizeOfTarget:
        print("Results generation for target ", el)
        thetaName = pathDataFolder + cmaesPath + "/ResCma" + str(el) + "/thetaCma" + str(el) + "TGUKF" + str(nameT)
        theta = np.loadtxt(thetaName)
        tgs = initAll(el, rs, True)
        cost = tgs.runTrajectoriesResultsGeneration(theta, nbret)
        print("Cost: ", cost)
        fileSavingAllDataJson(el, tgs.tg, nameFolderSave)
        #fileSavingAllData(el, tgs.tg)
    print("End of generation")
    
def generateResultsWithBestThetaTmp(nameFolderSave, nbret):
    rs = ReadSetupFile()
    listBT = getBestTheta()
    for el in listBT:
        print("Results generation for target ", el[0])
        theta = el[1]
        tgs = initAll(el[0], rs, True)
        cost = tgs.runTrajectoriesResultsGeneration(theta, nbret)
        print("Cost: ", cost)
        fileSavingAllDataJson(el[0], tgs.tg, nameFolderSave)
    print("End of generation")

def launchCMAESForSpecificTargetSize(sizeOfTarget):
    '''
    Run cmaes for a specific target size

    Input:	-sizeOfTarget, size of the target, float
    '''
    print("Starting the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    rs = ReadSetupFile()
    thetaLocalisation = pathDataFolder + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    #load the controller, ie the vector of parameters theta
    theta = np.loadtxt(thetaLocalisation)
    #normalize the vector
    theta = normalizationNP(theta, rs)
    #put theta to a one dimension numpy array, ie row vector form
    theta = matrixToVector(theta)
    #Initializes all the class used to generate trajectory
    tgs = initAll(sizeOfTarget, rs)
    #run the optimization (cmaes)
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, np.copy(theta), rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    #name used to save the new controller obtained by the optimization
    nameToSaveThetaCma = pathDataFolder + cmaesPath + "/ResCma" + str(sizeOfTarget) + "/"
    i = 1
    tryName = "thetaCma" + str(sizeOfTarget) + "TGUKF"
    for el in os.listdir(nameToSaveThetaCma):
        if tryName in el:
            i += 1
    tryName += str(i)
    nameToSaveThetaCma += tryName
    np.savetxt(nameToSaveThetaCma, resCma[0])
    print("End of optimization for target " + str(sizeOfTarget) + " !")
    
def launchCMAESWithBestThetaTmpForSpecificTargetSize(sizeOfTarget):
    '''
    Run cmaes for a specific target size with the best theta tmp

    Input:    -sizeOfTarget, size of the target, float
    '''
    print("Start of the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    rs = ReadSetupFile()
    listBT = getBestTheta()
    #get the best theta corresponding to the target size given
    for el in listBT:
        if el[0] == sizeOfTarget:
            theta = el[1]
    theta = normalizationNPWithoutSaving(theta, rs)
    theta = matrixToVector(theta)
    purgeCostNThetaTmp(sizeOfTarget)
    tgs = initAll(sizeOfTarget, rs)
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, np.copy(theta), rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    nameToSaveThetaCma = pathDataFolder + cmaesPath + "/ResCma" + str(sizeOfTarget) + "/"
    i = 1
    tryName = "thetaCma" + str(sizeOfTarget) + "TGUKF"
    for el in os.listdir(nameToSaveThetaCma):
        if tryName in el:
            i += 1
    tryName += str(i)
    nameToSaveThetaCma += tryName
    np.savetxt(nameToSaveThetaCma, resCma[0])
    print("End of optimization for target " + str(sizeOfTarget) + " !")

def launchCMAESWithBestThetaTmpForAllTargetSize():
    '''
    Launch in parallel cmaes optimization for each target size with the best theta temp
    '''
    rs = ReadSetupFile()
    p = Pool()
    p.map(launchCMAESWithBestThetaTmpForSpecificTargetSize, rs.sizeOfTarget)
    
def launchCMAESForAllTargetSize():
    '''
    Launch in parallel (on differents processor) the cmaes optimization for each target size
    '''
    #initializes fr (FileReading class) and rs (ReadSetup class) which allow to acces to setup variables and file reading functions
    rs = ReadSetupFile()
    #initializes a pool of worker, ie multiprocessing
    p = Pool()
    #run cmaes on each targets size on separate processor
    p.map(launchCMAESForSpecificTargetSize, rs.sizeOfTarget)





    
    
    
    
    
