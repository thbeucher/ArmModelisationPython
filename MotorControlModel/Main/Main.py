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
from Utils.ThetaNormalization import normalization, unNormalization

from ArmModel.Arm import Arm
from Experiments.Experiments import Experiments, copyRBFNtoCMAES

def GenerateDataFromTheta(rs,sizeOfTarget, foldername, thetaFile, repeat, save):
    exp = Experiments(rs, sizeOfTarget, save, foldername,thetaFile)
    cost = exp.runTrajectoriesResultsGeneration(repeat)
    print("Average cost: ", cost)
    print("foldername : ", foldername)
    if (save):
        exp.saveCost()

def generateFromCMAES(repeat, thetaFile, saveDir = 'Data'):
    rs = ReadSetupFile()
    for el in rs.sizeOfTarget:
        thetaName = rs.CMAESpath + str(el) + "/" + thetaFile
        saveName = rs.CMAESpath + str(el) + "/" + saveDir + "/"
        GenerateDataFromTheta(rs,el,saveName,thetaName,repeat,True)
    print("CMAES:End of generation")

def generateFromRBFN(repeat, thetaFile, saveDir):
    rs = ReadSetupFile()
    thetaName = rs.RBFNpath + thetaFile
    saveName = rs.RBFNpath + saveDir + "/"
    GenerateDataFromTheta(rs,0.1,saveName,thetaName,repeat,True)
    print("RBFN:End of generation")

def launchCMAESForSpecificTargetSize(sizeOfTarget, thetaFile):
    '''
    Run cmaes for a specific target size

    Input:	-sizeOfTarget, size of the target, float
    '''
    print("Starting the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    rs = ReadSetupFile()
    foldername = rs.CMAESpath + str(sizeOfTarget) + "/"
    thetaname = foldername + thetaFile

    #Initializes all the class used to generate trajectory
    exp = Experiments(rs, sizeOfTarget, False, foldername, thetaname)
    theta = exp.tm.controller.theta
    thetaIn = theta.flatten()
    thetaCMA, max = normalization(thetaIn)
    exp.maxT = max
    print ("max normalisation :", max)
    print (theta CMA : ", thetaCMA)

    #run the optimization (cmaes)
    resCma = cma.fmin(exp.runTrajectoriesCMAES, thetaCMA, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    exp.call = 0
    print("End of optimization for target " + str(sizeOfTarget) + " !")
    
def launchCMAESForAllTargetSizes(thetaname, save):
    rs = ReadSetupFile()
    if save:
        copyRBFNtoCMAES(rs, thetaname)
    for el in rs.sizeOfTarget:
        launchCMAESForSpecificTargetSize(el, thetaname)

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





    
    
    
    
    
