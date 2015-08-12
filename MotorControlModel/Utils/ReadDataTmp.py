#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher
Module: ReadDataTmp
Description: the function below alow to read temporary data
'''

import numpy as np
from GlobalVariables import pathDataFolder, cmaesPath

def readThetaTmpBySizeOfTarget(sizeOfTarget, rs):
    dim0 = rs.numfeats**rs.inputDim
    nameFileToRead = pathDataFolder + cmaesPath + "/ResCma" + str(sizeOfTarget) + "/thetaSolTmp_target" + str(sizeOfTarget)
    f = open(nameFileToRead, 'r')
    try:
        arrAll = np.loadtxt(f)
        numberOfTheta = arrAll.shape[0]/dim0
        arrList = np.split(arrAll, numberOfTheta)
    except:
        arrList = "None"
    return arrList

def readCostTmpBySizeOfTarget(sizeOfTarget):
    nameFileToRead = pathDataFolder + cmaesPath + "/ResCma" + str(sizeOfTarget) + "/meanCost" + str(sizeOfTarget)
    try:
        costList = np.loadtxt(nameFileToRead)
    except:
        costList = "None"
    return costList


def getBestTheta():
    rs = ReadSetupFile()
    listBT = []
    for el in rs.sizeOfTarget:
        listT = readThetaTmpBySizeOfTarget(el, rs)
        listC = readCostTmpBySizeOfTarget(el)
        if listC == "None":
            bestTheta = "None"
        else:
            costMaxIndice = np.argmax(listC)
            bestTheta = listT[costMaxIndice]
        listBT.append((el, bestTheta))   
    return listBT
        
    



