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

from Utils.ThetaNormalization import normalizationNP, matrixToVector, normalizationNPWithoutSaving
from Utils.ReadDataTmp import getBestTheta
from Utils.ReadSetupFile import ReadSetupFile
from Utils.PurgeData import purgeCostNThetaTmp

from ArmModel.Arm import Arm
from Experiments.Experiments import Experiments

def GenerateDataFromTheta(sizeOfTarget, thetaLoadFile, foldername, repeat, rs):
    theta = np.loadtxt(thetaLoadFile)
    theta = normalizationNP(theta)
    exp = Experiments(rs, sizeOfTarget, True, foldername)
    cost = exp.runTrajectoriesResultsGeneration(theta, repeat)
    print("Cost: ", cost)
    exp.saveCost(foldername)

def generateFromCMAES(repeat, thetaFile, saveDir = 'Data'):
    rs = ReadSetupFile()
    for el in rs.sizeOfTarget:
        thetaName = rs.CMAESpath + str(el) + "/" + thetaFile
        saveName = rs.CMAESpath + str(el) + "/" + saveDir + "/"
        GenerateDataFromTheta(el,thetaName,saveName,repeat,rs)
    print("CMAES:End of generation")

def generateFromRBFN(repeat, thetaFile, saveDir = 'Data'):
    rs = ReadSetupFile()
    thetaName = rs.RBFNpath + thetaFile
    saveName = rs.RBFNpath + saveDir + "/"
    GenerateDataFromTheta(0.1,thetaName,saveName,repeat,rs)
    print("RBFN:End of generation")

#------------------------- not updated -------------------------------------
    
def generateOneTrajFromRBFN(folderName, saveFile = 'None'):
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
    exp = Experiments(rs, rs.sizeOfTarget[3], True, foldername)
    cost = exp.runOneTrajectory(theta, coord)
    print("Cost: ", cost)
    exp.saveCost(foldername)
    print("End of generation")

def generateResultsWithBestThetaTmp(folderName, nbret):
    rs = ReadSetupFile()
    listBT = getBestTheta()
    for el in listBT:
        print("Results generation for target ", el[0])
        theta = el[1]
        exp = Experiments(rs,el[0], True, foldername)
        cost = exp.runTrajectoriesResultsGeneration(theta, nbret)
        print("Cost: ", cost)
        exp.saveCost(foldername)
    print("End of generation")

def launchCMAESForSpecificTargetSize(sizeOfTarget, thetaFile):
    '''
    Run cmaes for a specific target size

    Input:	-sizeOfTarget, size of the target, float
    '''
    print("Starting the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    rs = ReadSetupFile()
    foldername = rs.CMAESpath + str(sizeOfTarget) + "/"
    thetaLocalisation =  foldername + thetaFile
    #load the controller, ie the vector of parameters theta
    theta = np.loadtxt(thetaLocalisation)
    #normalize the vector
    theta = normalizationNP(theta)
    #put theta to a one dimension numpy array, ie row vector form
    theta = matrixToVector(theta)
    #Initializes all the class used to generate trajectory
    exp = Experiments(rs, sizeOfTarget, True, foldername)
    #run the optimization (cmaes)
    resCma = cma.fmin(exp.runTrajectoriesCMAES, np.copy(theta), rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
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





    
    
    
    
    
