#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher
Module: ReadDataTmp
Description: the function below alow to read temporary data
'''

import numpy as np
from GlobalVariables import pathDataFolder
from Utils.InitUtil import initFRRS


def readThetaTmpBySizeOfTarget(sizeOfTarget, rs):
    dim0 = rs.numfeats**rs.inputDim
    nameFileToRead = pathDataFolder + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/thetaSolTmp_target" + str(sizeOfTarget)
    f = open(nameFileToRead, 'r')
    arrAll = np.loadtxt(f)
    numberOfTheta = arrAll.shape[0]/dim0
    arrList = np.split(arrAll, numberOfTheta)
    return arrList

def readCostTmpBySizeOfTarget(sizeOfTarget):
    nameFileToRead = pathDataFolder + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/meanCost" + str(sizeOfTarget)
    costList = np.loadtxt(nameFileToRead)
    return costList


def getBestTheta():
    fr, rs = initFRRS()
    listBT = []
    for el in rs.sizeOfTarget:
        listT = readThetaTmpBySizeOfTarget(el, rs)
        listC = readCostTmpBySizeOfTarget(el)
        costMaxIndice = np.argmax(listC)
        bestTheta = listT[costMaxIndice]
        listBT.append((el, bestTheta))   
    return listBT
        
    



