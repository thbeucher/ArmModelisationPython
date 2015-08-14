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
from Utils.FileReading import getStateDataFromBrent, getInitPos, getobjread, getobjreadJson
from Utils.FileSaving import saveBin, saveStr
from Utils.ThetaNormalization import normalization, matrixToVector, vectorToMatrix, unNorm

from GlobalVariables import BrentTrajectoriesFolder, pathDataFolder

def checkReachAllTarget(folderName):
    rs = ReadSetupFile()
    listOfDic = []
    for el in rs.sizeOfTarget:
        dicTmp = checkIfTargetIsReach(el, folderName)
        for key, val in dicTmp.items():
            i = 0
            for elt in val:
                if elt == 1:
                    i += 1
            dicTmp[key] = i*100/len(val)
        listOfDic.append(dicTmp)
    print(listOfDic)
        
    
def timeDistance():
    rs = ReadSetupFile()
    name = rs.RBFNpath + "nbIteBIN" 
    data = getobjread(name)
    key = []
    for el in data.keys():
        key.append(el.split("//"))
    for i in range(len(key)):
        key[i][0] = float(key[i][0])
        key[i][1] = float(key[i][1])
    r = []
    for el in key:
        r1 = math.sqrt(((tronquerNB(el[0], 5)**2) + ((tronquerNB(el[1], 5) - rs.targetOrdinate)**2)))/2
        r.append(tronquerNB(r1, 2))
    

def returnX0Y0Z(name):
    rs = ReadSetupFile()
    zdico = getobjread(name + "costTrajRBFNBIN")
    xAbn, yAbn, zWithoutAbn, xyAbn, valcost = [], [], [], [], []
    for key,el in zdico.items():
        if not el < 200:
            xAbn.append(tronquerNB(float(key.split("//")[0]), 3))
            yAbn.append(tronquerNB(float(key.split("//")[1]), 3))
            xyAbn.append((tronquerNB(float(key.split("//")[0]), 3), tronquerNB(float(key.split("//")[1]), 3)))
            valcost.append(el-rs.rhoCF)
        else:
            zWithoutAbn.append(el)
    x0, y0 = [], []
    for el in xyAbn:
        x0.append(el[0])
        y0.append(el[1])
    z = valcost
    if not z:
        x0 = []
        y0 = []
        posi = getobjread(rs.experimentFilePosIni)
        for el in posi:
            x0.append(el[0])
            y0.append(el[1])
        z = getobjread(name + "costBIN")
    return x0, y0, z

def returnDifCostBrentRBFN():
    rs = ReadSetupFile()
    name = rs.RBFNpath + "costTrajBIN"
    RBFN = getobjread(name)
    Brent = getobjread("trajectoires_cout/trajectoire_coutCoordXBIN")
    dataRBFN, dataBrent, xyRBFN, xyBrent = [], [], [], []
    for el in Brent:
        dataBrent.append((el[2], el[3], el[1]))
        xyBrent.append((el[2], el[3]))
    for key, el in RBFN.items():
        dataRBFN.append((tronquerNB(float(key.split("//")[0]), 3), tronquerNB(float(key.split("//")[1]), 3), el))
        xyRBFN.append((tronquerNB(float(key.split("//")[0]), 3), tronquerNB(float(key.split("//")[1]), 3)))
    difAllPts = []
    for el in xyBrent:
        if el in xyRBFN:
            a = np.abs(dataBrent[xyBrent.index(el)][2] - dataRBFN[xyRBFN.index(el)][2])
            difAllPts.append((el[0], el[1], a))
    saveStr(name + "difCostBrentRBFN", difAllPts)
    saveBin(name + "difCostBrentRBFNBIN", difAllPts)
    return difAllPts

def checkForDoublonInTraj(localisation):
    '''
    
    Input:    -localisation: String, path given the folder where the trajectories are
    '''
    rs = ReadSetupFile()
    data, junk = getInitPos(localisation)
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

def posCircle(r, t):
    '''
    give coordinate (x,y) from couple (radius, angle)
    
    Input:      -r: scalar, radius of the circle
                -t: scalar, angle
    
    Output:    -x: scalar, ordinate
                -y: scalar, absciss
    '''
    rs = ReadSetupFile()
    x0 = 0
    y0 = rs.targetOrdinate
    x = x0 + r * math.cos(t)
    y = y0 + r * math.sin(t)
    return x, y

def invPosCircle(x, y):
    '''
    give couple (radius, angle) from coordinate (x, y), here the center of the circle is (0, yt) (yt = 0.6175)
    
    Input:      -x: scalar, ordinate
                -y: scalar, absciss
    
    Output:     -r: scalar, radius of the circle
                -t: scalar, angle
    '''
    rs = ReadSetupFile()
    r = math.sqrt((x**2) + (y - rs.targetOrdinate)**2)
    t = math.atan2(y - rs.targetOrdinate, x)
    return r, t

def remakeTrajFolder():
    rs = ReadSetupFile()
    for el in os.listdir(pathDataFolder + "/trajNotUsedTmp/"):
        copyfile(pathDataFolder + "/trajNotUsedTmp/" + el, BrentTrajectoriesFolder + el)
        remove(pathDataFolder + "/trajNotUsedTmp/" + el)

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

def testNPDOT():
    try:
        import numpy.core._dotblas
        print ('FAST BLAS')
    except ImportError:
        print ('slow blas')
     
    print ("version:", numpy.__version__)
    #print ("maxint:", sys.maxint)
    #print
     
    x = numpy.random.random((1000,1000))
     
    setup = "import numpy; x = numpy.random.random((1000,1000))"
    count = 5
     
    t = timeit.Timer("numpy.dot(x, x.T)", setup=setup)
    print ("dot:", t.timeit(count)/count, "sec")
        
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


#---------------------- velocity profiles --------------------------------------------------------------

def getVelocityProfileData(folderName):
    rs = ReadSetupFile()
    name = folderName + "/saveSpeed"
    nameNbIte = folderName + "/saveNumberOfIteration"

    data = getobjreadJson(name)
    nbIte = getobjreadJson(nameNbIte)
    aAll, vAll, tAll = {}, {}, {}
    for key, val in data.items():
        a = []
        for i in range(nbIte[key][0]):
            a.append(data[key][0][i])
        aAll[key] = a
    for key, val in aAll.items():
        vtmp = []
        for el in val:
            vtmp.append(np.linalg.norm(el))
        vAll[key] = vtmp
    for key, val in vAll.items():
        ttmp = []
        for i in range(len(val)):
            ttmp.append(i)
        tAll[key] = ttmp
    return tAll, vAll

#---------------------- end of velocity profiles --------------------------------------------------------------

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

def checkIfTargetIsReach(sizeOfTarget, folderName):
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
    


    

