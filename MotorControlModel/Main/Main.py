#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: Main

Description: We find here functions usefull to run cmaes and latter some script to run trajectories
'''

import cma
import numpy as np
from multiprocessing.pool import Pool
from Utils.InitUtil import initFRRS
from Utils.ThetaNormalization import normalizationNP, matrixToVector,\
    normalizationNPWithoutSaving
from Utils.InitUtilMain import initAllUsefullObj
from Utils.FileSaving import fileSavingAllDataJson
from GlobalVariables import pathDataFolder
import os
from Utils.ReadDataTmp import getBestTheta
from Utils.PurgeData import purgeCostNThetaTmp

def generateTrajectoryRBFN(nameFolder, nameT = 'None'):
    fr, rs = initFRRS()
    if nameT == 'None':
        nameTheta = pathDataFolder + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    else:
        nameTheta = pathDataFolder + "RBFN2/" + str(rs.numfeats) + "feats/" + nameT
    theta = np.loadtxt(nameTheta)
    print("Enter coordinate of the initial point!")
    x = input("x: ")
    x = float(x)
    y = input("y: ")
    y = float(y)
    coord = (x, y)
    tgs = initAllUsefullObj(rs.sizeOfTarget[3], fr, rs, True)
    cost = tgs.runOneTrajectoryRBFN(theta, coord)
    print("Cost: ", cost)
    fileSavingAllDataJson(0, tgs.tg, nameFolder, True)
    print("End of generation")
    
    
def generateResults(nameFolderSave, nbret, nameT):
    fr, rs = initFRRS()
    for el in rs.sizeOfTarget:
        print("Results generation for target ", el)
        thetaName = pathDataFolder + "OptimisationResults/ResCma" + str(el) + "/thetaCma" + str(el) + "TGUKF" + nameT
        theta = np.loadtxt(thetaName)
        tgs = initAllUsefullObj(el, fr, rs, True)
        cost = tgs.runTrajectoriesResultsGeneration(theta, nbret)
        print("Cost: ", cost)
        fileSavingAllDataJson(el, tgs.tg, nameFolderSave)
        #fileSavingAllData(el, tgs.tg)
    print("End of generation")
    
def generateResultsWithBestThetaTmp(nameFolderSave, nbret):
    fr, rs = initFRRS()
    listBT = getBestTheta()
    for el in listBT:
        print("Results generation for target ", el[0])
        theta = el[1]
        tgs = initAllUsefullObj(el[0], fr, rs, True)
        cost = tgs.runTrajectoriesResultsGeneration(theta, nbret)
        print("Cost: ", cost)
        fileSavingAllDataJson(el[0], tgs.tg, nameFolderSave)
    print("End of generation")

def launchCMAESForSpecificTargetSize(sizeOfTarget):
    '''
    Run cmaes for a specific target size

    Input:	-sizeOfTarget, size of the target, float
    '''
    print("Start of the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    fr, rs = initFRRS()
    thetaLocalisation = pathDataFolder + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    #load the controller, ie the vector of parameters theta
    theta = np.loadtxt(thetaLocalisation)
    #normalize the vector
    theta = normalizationNP(theta, rs)
    #put theta to a one dimension numpy array, ie row vector form
    theta = matrixToVector(theta)
    #Initializes all the class used to generate trajectory
    tgs = initAllUsefullObj(sizeOfTarget, fr, rs)
    #run the optimization (cmaes)
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, np.copy(theta), rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    #name used to save the new controller obtained by the optimization
    nameToSaveThetaCma = pathDataFolder + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/"
    #thetaCma" + str(sizeOfTarget) + "TGUKF1"
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
    fr, rs = initFRRS()
    listBT = getBestTheta()
    #get the best theta corresponding to the target size given
    for el in listBT:
        if el[0] == sizeOfTarget:
            theta = el[1]
    theta = normalizationNPWithoutSaving(theta, rs)
    theta = matrixToVector(theta)
    purgeCostNThetaTmp(sizeOfTarget)
    tgs = initAllUsefullObj(sizeOfTarget, fr, rs)
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, np.copy(theta), rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    nameToSaveThetaCma = pathDataFolder + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/"
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
    fr, rs = initFRRS()
    p = Pool()
    p.map(launchCMAESWithBestThetaTmpForSpecificTargetSize, rs.sizeOfTarget)
    
def launchCMAESForAllTargetSize():
    '''
    Launch in parallel (on differents processor) the cmaes optimization for each target size
    '''
    #initializes fr (FileReading class) and rs (ReadSetup class) which allow to acces to setup variables and file reading functions
    fr, rs =initFRRS()
    #initializes a pool of worker, ie multiprocessing
    p = Pool()
    #run cmaes on each targets size on separate processor
    p.map(launchCMAESForSpecificTargetSize, rs.sizeOfTarget)





    
    
    
    
    
