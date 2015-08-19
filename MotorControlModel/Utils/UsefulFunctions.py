#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: UsefulFunctions

Description: global variables used in the project
'''
import os
import math
import numpy as np
from shutil import copyfile
from posix import remove
import timeit

from Utils.NiemRoot import tronquerNB
from Utils.ReadSetupFile import ReadSetupFile
from Utils.FileReading import getInitPos

from GlobalVariables import BrentTrajectoriesFolder, pathDataFolder

def checkReachAllTarget(folderName):
    rs = ReadSetupFile()
    listOfDic = []
    for el in rs.sizeOfTarget:
        dicTmp = checkIfTargetIsReached(el, folderName)
        for key, val in dicTmp.items():
            i = 0
            for elt in val:
                if elt == 1:
                    i += 1
            dicTmp[key] = i*100/len(val)
        listOfDic.append(dicTmp)
    print(listOfDic)
    
def getDifCost(what1,what2):
    rs = ReadSetupFile()

    if what1 == "CMAES":
        name1 = rs.CMAESpath + targetSize + folderName + "/Cost/"
    elif what1 == "Brent":
        name1 = BrentTrajectoriesFolder
    else:
        name1 = rs.RBFNpath + folderName + "/Cost/"

    if what2 == "CMAES":
        name2 = rs.CMAESpath + targetSize + folderName + "/Cost/"
    elif what2 == "Brent":
        name2 = BrentTrajectoriesFolder
    else:
        name2 = rs.RBFNpath + folderName + "/Cost/"

    costs1 = getCostData(name1)
    costs2 = getCostData(name2)

    #Note: todo : indexer par xy pour retrouver les couts correspondants
    x0 = []
    y0 = []
    cost = []

    for k, v in costs1.items():
        for j in range(len(v)):
            x0.append(v[j][0])
            y0.append(v[j][1])
            cost.append(v[j][2]-costs2[2])

    return dif

def checkForDoublonInTraj(localisation):
    '''
    
    Input:    -localisation: String, path given the folder where the trajectories are
    '''
    rs = ReadSetupFile()
    data = getInitPos(localisation)
    tabEl, doublon = [], []
    for key, el in data.items():
        if el in tabEl:
            doublon.append(key)
            #copyfile(localisation + key, localisation + "doublon/" + key)
            #remove(localisation + key)
        else:
            tabEl.append(el)
    print("ici", len(doublon), doublon)
    c = input("cc")
    print("la", len(tabEl), tabEl)

def checkIfTargetIsReached(sizeOfTarget, folderName):
    name = rs.CMAESpath + str(sizeOfTarget) + "/" + folderName + "/saveCoordEndTraj"
    data = getobjreadJson(name)
    targetReachOrNot = {}
    for key, val in data.items():
        targetReachOrNot[key] = []
        for el in val:
            if el[0] >= -sizeOfTarget/2 and el[0] <= sizeOfTarget/2:
                targetReachOrNot[key].append(1)
            else:
                targetReachOrNot[key].append(0)
    return targetReachOrNot
    


    

