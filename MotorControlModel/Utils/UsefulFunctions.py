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
from Utils.ThetaNormalization import matrixToVector, vectorToMatrix

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
    
def returnDifCost(what1,what2):
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
    for k, v in costs.items():
        x0.append(v[0])
        y0.append(v[1])
        cost.append(costs2[2]-costs1[2])

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

def getTimeDistance(sizeTarget, folderName, rbfn = False):
    rs = ReadSetupFile()
    if rbfn == False:
        name = rs.CMAESpath + str(sizeTarget) + "/" + folderName + "/saveNumberOfIteration"
    else:
        name = rs.RBFNpath + folderName + "/saveNumberOfIteration"
    nbIteTraj = getobjreadJson(name)
    distTimeDico = {}
    for key, val in nbIteTraj.items():
        nbIteTraj[key] = int(np.mean(nbIteTraj[key]))
        r, t = invPosCircle(float(key.split("//")[0]), float(key.split("//")[1]))
        r = round(r, 2)
        if not r in distTimeDico.keys():
            distTimeDico[r] = []
        distTimeDico[r].append(nbIteTraj[key])
    distTime = []
    for key, val in distTimeDico.items():
        distTimeDico[key] = int(np.mean(distTimeDico[key]))
        distTime.append((key, distTimeDico[key]))
    return distTime
        
def getDataScattergram(sizeT, nameFolder):
    rs = ReadSetupFile()
    name = rs.CMAESpath + str(sizeT) + "/" + nameFolder + "/hitDispersion"
    coordHit = getobjread(name)
    allX = []
    for key, val in coordHit.items():
        xByPosIni = [x[0] for x in val]
        allX.append(xByPosIni)
    s = 0
    for el in allX:
        if s == 0:
            allXArray = np.asarray(el)
            s += 1
        else:
            allXArray = np.hstack((allXArray, el))
    return allXArray

def getDistPerfSize(sizeT, folderName, rbfn = False):
    rs = ReadSetupFile()
    if rbfn == False:
        name = rs.CMAESpath + str(sizeT) + "/" + folderName + "/saveU"
    else:
        name = rs.RBFNpath + folderName + "/saveU"

    data = getobjreadJson(name)
    DistPerf = {}
    for key, val in data.items():
        r, t = invPosCircle(float(key.split("//")[0]), float(key.split("//")[1]))
        r = round(r, 2)
        if not r in DistPerf.keys():
            DistPerf[r] = []
        DistPerf[r].append(np.mean(val[0]))
    for key, val in DistPerf.items():
        DistPerf[key] = np.mean(val)
    sizeDistPerf = []
    for key, val in DistPerf.items():
        sizeDistPerf.append((sizeT, key, val))
    return sizeDistPerf

def getTimeByArea(sizeT, folderName, rbfn = False):
    rs = ReadSetupFile()
    if rbfn == False:
        name = rs.CMAESpath + str(sizeT) + "/" + folderName + "/saveNumberOfIteration"
    else:
        name = rs.RBFNpath + folderName + "/saveNumberOfIteration"
    data = getobjreadJson(name)
    areaTime = []
    for key, val in data.items():
        areaTime.append((round(float(key.split("//")[0]), 4), round(float(key.split("//")[1]), 4), int(np.mean(val))))
    return areaTime

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
    


    

