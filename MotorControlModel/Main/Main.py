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
from Utils.FileSaving import saveAllData
from Utils.ReadDataTmp import getBestTheta
from Utils.ReadSetupFile import ReadSetupFile
from Utils.PurgeData import purgeCostNThetaTmp

from ArmModel.Arm import Arm

from Regression.functionApproximator_RBFN import fa_rbfn

from Kalman.UnscentedKalmanFilterControl import UnscentedKalmanFilterControl
from TrajectoryGenerator.TrajectoryGenerator import TrajectoryGenerator
from Experiments.Experiments import Experiments
from CostComputation.CostComputation import CostComputation
from GlobalVariables import BrentTrajectoriesFolder, pathDataFolder

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
    #fa, function approximator i.e. the controller
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

def GenerateDataFromTheta(sizeOfTarget, thetaLoadFile, dataSaveDir, repeat, rs):
    theta = np.loadtxt(thetaLoadFile)
    theta = normalizationNP(theta)
    exp = initAll(sizeOfTarget, rs, True)
    cost = exp.runTrajectoriesResultsGeneration(theta, repeat)
    print("Cost: ", cost)
    saveAllData(sizeOfTarget, exp.tg, dataSaveDir)

def generateFromCMAES(repeat, thetaFile, saveDir = 'Data/'):
    rs = ReadSetupFile()
    for el in rs.sizeOfTarget:
        thetaName = rs.CMAESpath + str(el) + "/" + thetaFile
        saveName = rs.CMAESpath + str(el) + "/" + saveDir
        GenerateDataFromTheta(el,thetaName,saveName,repeat,rs)
    print("CMAES:End of generation")

def generateFromRBFN(repeat, thetaFile, saveDir = 'Data/'):
    rs = ReadSetupFile()
    thetaName = rs.RBFNpath + thetaFile
    saveName = rs.RBFNpath + saveDir
    GenerateDataFromTheta(0.1,thetaName,saveName,repeat,rs)
    print("RBFN:End of generation")

#------------------------- not updated -------------------------------------
    
def generateOneTrajFromRBFN(nameFolder, saveFile = 'None'):
    rs = ReadSetupFile()
    if saveFile == 'None':
        thetaName = rs.RBFNpath + "ThetaX7NP"
    else:
        thetaName = rs.RBFNpath + saveFile
    theta = np.loadtxt(thetaName)
    print("Enter coordinate of the initial point!")
    x = input("x: ")
    x = float(x)
    y = input("y: ")
    y = float(y)
    coord = (x, y)
    exp = initAll(rs.sizeOfTarget[3], rs, True)
    cost = exp.runOneTrajectory(theta, coord)
    print("Cost: ", cost)
    saveAllData(0, exp.tg, nameFolder, True)
    print("End of generation")

def generateResultsWithBestThetaTmp(nameFolderSave, nbret):
    rs = ReadSetupFile()
    listBT = getBestTheta()
    for el in listBT:
        print("Results generation for target ", el[0])
        theta = el[1]
        exp = initAll(el[0], rs, True)
        cost = exp.runTrajectoriesResultsGeneration(theta, nbret)
        print("Cost: ", cost)
        saveAllData(el[0], exp.tg, nameFolderSave)
    print("End of generation")

def launchCMAESForSpecificTargetSize(sizeOfTarget, thetaFile):
    '''
    Run cmaes for a specific target size

    Input:	-sizeOfTarget, size of the target, float
    '''
    print("Starting the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    rs = ReadSetupFile()
    thetaLocalisation =  rs.CMAESpath + str(sizeOfTarget) + "/" + thetaFile
    #load the controller, ie the vector of parameters theta
    theta = np.loadtxt(thetaLocalisation)
    #normalize the vector
    theta = normalizationNP(theta)
    #put theta to a one dimension numpy array, ie row vector form
    theta = matrixToVector(theta)
    #Initializes all the class used to generate trajectory
    exp = initAll(sizeOfTarget, rs)
    #run the optimization (cmaes)
    resCma = cma.fmin(exp.runTrajectoriesCMAES, np.copy(theta), rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    #name used to save the new controller obtained by the optimization
    nameToSaveThetaCma = rs.CMAESpath + str(sizeOfTarget) + "/"
    i = 1
    tryName = "thetaCma" + str(sizeOfTarget) + "save"
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
    theta = normalizationNPWithoutSaving(theta)
    theta = matrixToVector(theta)
    purgeCostNThetaTmp(sizeOfTarget)
    exp = initAll(sizeOfTarget, rs)
    resCma = cma.fmin(exp.runTrajectoriesCMAES, np.copy(theta), rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    nameToSaveThetaCma = rs.CMAESpath + str(sizeOfTarget) + "/"
    i = 1
    tryName = "thetaCma" + str(sizeOfTarget) + "TGUKF"
    for el in os.listdir(nameToSaveThetaCma):
        if tryName in el:
            i += 1
    tryName += str(i)
    nameToSaveThetaCma += tryName
    np.savetxt(nameToSaveThetaCma, resCma[0])
    print("End of optimization for target " + str(sizeOfTarget) + " !")
    
def launchCMAESForAllTargetSizes():
    rs = ReadSetupFile()
    for el in rs.sizeOfTarget:
        launchCMAESForSpecificTargetSize(el, "theta")

#--------------------------- multiprocessing -------------------------------------------------------

def launchCMAESWithBestThetaTmpForAllTargetSize():
    '''
    Launch in parallel cmaes optimization for each target size with the best theta temp
    '''
    #initializes setup variables
    rs = ReadSetupFile()
    #initializes a pool of worker, ie multiprocessing
    p = Pool()
    #run cmaes on each targets size on separate processor
    p.map(launchCMAESWithBestThetaTmpForSpecificTargetSize, rs.sizeOfTarget)
    
def launchCMAESForAllTargetSizesMulti():
    '''
    Launch in parallel (on differents processor) the cmaes optimization for each target size
    '''
    #initializes setup variables
    rs = ReadSetupFile()
    #initializes a pool of worker, ie multiprocessing
    p = Pool()
    #run cmaes on each targets size on separate processor
    p.map(launchCMAESForSpecificTargetSize, rs.sizeOfTarget, "theta")





    
    
    
    
    
