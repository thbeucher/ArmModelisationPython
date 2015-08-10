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
from Utils.ThetaNormalization import normalizationNP, matrixToVector
from Utils.InitUtilMain import initAllUsefullObj
from Utils.FileSaving import fileSavingAllData
from GlobalVariables import pathDataFolder

def generateResults(nameFolderSave, nbret):
    fr, rs = initFRRS()
    for el in rs.sizeOfTarget:
        print("Results generation for target ", el)
        thetaName = pathDataFolder + "OptimisationResults/ResCma" + str(el) + "/thetaCma" + str(el) + nameFolderSave
        theta = np.loadtxt(thetaName)
        tgs = initAllUsefullObj(el, fr, rs)
        cost = tgs.runTrajectoriesResultsGeneration(theta, nbret)
        print("Cost: ", cost)
        fileSavingAllData(el, tgs.tg)
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
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, theta, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    #name used to save the new controller obtained by the optimization
    nameToSaveThetaCma = pathDataFolder + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/thetaCma" + str(sizeOfTarget) + "TGUKF1"
    np.savetxt(nameToSaveThetaCma, resCma[0])
    print("End of optimization for target " + str(sizeOfTarget) + " !")
    
def launchCMAESForAllTargetSize():
    '''
    Launch in parallel (on differents processor) the cmaes optimization for each target size
    '''
    #initializes fr (FileReading class) and rs (ReadSetup class) which allow to acces to setup variables and file reading functions
    fr, rs =initFRRS()
    #initializes a pool of worker, ie multiprocessing
    p = Pool(4)
    #run cmaes on each targets size on separate processor
    p.map(launchCMAESForSpecificTargetSize, rs.sizeOfTarget)





    
    
    
    
    
