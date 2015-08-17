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

from Utils.ReadSetupFile import ReadSetupFile

from ArmModel.Arm import Arm
from Experiments.Experiments import Experiments

def GenerateDataFromTheta(rs,sizeOfTarget, foldername, thetaFile, repeat):
    exp = Experiments(rs, sizeOfTarget, True, foldername,thetaFile)
    cost = exp.runTrajectoriesResultsGeneration(repeat)
    print("CostArray: ", cost)
    print("foldername : ", foldername)
    exp.saveCost()

def generateFromCMAES(repeat, thetaFile, saveDir = 'Data'):
    rs = ReadSetupFile()
    thetaName = rs.RBFNpath + thetaFile
    for el in rs.sizeOfTarget:
        saveName = rs.CMAESpath + str(el) + "/" + saveDir + "/"
        GenerateDataFromTheta(rs,el,saveName,thetaName,repeat)
    print("CMAES:End of generation")

def generateFromRBFN(repeat, thetaFile, saveDir):
    rs = ReadSetupFile()
    thetaName = rs.RBFNpath + thetaFile
    saveName = rs.RBFNpath + saveDir + "/"
    GenerateDataFromTheta(rs,0.1,saveName,thetaName,repeat)
    print("RBFN:End of generation")

def launchCMAESForSpecificTargetSize(sizeOfTarget, thetaFile):
    '''
    Run cmaes for a specific target size

    Input:	-sizeOfTarget, size of the target, float
    '''
    print("Starting the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    rs = ReadSetupFile()
    foldername = rs.CMAESpath + str(sizeOfTarget) + "/"
    thetaname = foldername + thetafile

    #Initializes all the class used to generate trajectory
    exp = Experiments(rs, sizeOfTarget, True, foldername, thetaname)
    theta = exp.tm.theta
    #run the optimization (cmaes)
    resCma = cma.fmin(exp.runTrajectoriesCMAES, theta, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    #name used to save the controller obtained from optimization
    i = 1
    tryName = "thetaCma" + str(sizeOfTarget) + "save"
    for el in os.listdir(foldername):
        if tryName in el:
            i += 1
            tryName += str(i)
        nameToSaveThetaCma += tryName
        np.savetxt(foldername, resCma[0])
    theta = resCma[0]
    print("end loop step")

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





    
    
    
    
    
