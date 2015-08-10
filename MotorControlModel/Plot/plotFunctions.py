#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: plotFunctions

Description: some plotting functions
'''

import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.mlab import griddata

import os
from ArmModel.GeometricModel import mgd
import math
from Utils.NiemRoot import tronquerNB
from Utils.InitUtil import initFRRS
from Utils.FileReading import FileReading

from Utils.UsefulFunctions import returnX0Y0Z, returnDifCostBrentRBFN,\
     getTimeDistance, getDistPerfSize, getVelocityProfileDataRBFN, getVelocityProfileDataCMAES, getTimeByArea,\
    checkIfTargetIsReach

from GlobalVariables import BrentTrajectoriesFolder, pathDataFolder

def costColorPlot(what):
    '''
    Cette fonction permet d'afficher le profil de cout des trajectoires
    
    Entrees:    -nbfeat: nombre de features utilises pour generer le controleur actuel
                -what: choix des donnees a afficher
    '''
    xt = 0
    
    fr, rs = initFRRS()
    nbfeat = rs.numfeats
    
    x0 = []
    y0 = []
    posi = fr.getobjread(rs.experimentFilePosIni)
    for el in posi:
        x0.append(el[0])
        y0.append(el[1])
        
    if what == "rbfn":
        name = "RBFN2/" + str(nbfeat) + "feats/"
        x0, y0, z = returnX0Y0Z(name)
        
    elif what == "cma":
        name = "RBFN2/" + str(nbfeat) + "feats/costBINCma"
        z = fr.getobjread(name)
        for i in range(len(z)):
            if z[i] > 0:
                z[i] -= rs.rhoCF
        
    elif wha == "brent":
        data = fr.getobjread("trajectoires_cout/trajectoire_coutCoordXBIN")
        z, x0, y0 = [], [], []
        for el in data:
            z.append(el[1]-rs.rhoCF)
            x0.append(el[2])
            y0.append(el[3])
    
    elif what == "difBR":
        dif = returnDifCostBrentRBFN()
        z, zobj, x0, y0 = [], [], [], []
        for el in dif:
            if el[2] < 10:
                z.append(el[2])
                zobj.append(el)
                x0.append(el[0])
                y0.append(el[1])
    
    zb = z
    xi = np.linspace(-0.25,0.25,100)
    yi = np.linspace(0.35,0.5,100)
    er = 0
    try:
        zb.shape[1]
    except IndexError:
        er = 1
    except AttributeError:
        er = 1
    if type(zb) == type([]):
        zi = griddata(x0, y0, zb, xi, yi)
    elif er == 1:
        zi = griddata(x0, y0, zb, xi, yi)
    else:
        zi = griddata(x0, y0, zb.T[0], xi, yi)
    
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=zb, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    CS = plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t1, shrink=0.5, aspect=5)
    plt.show(block = True)

def plotHitDispersion(sizeT):
    fr, rs = initFRRS()
    #name = "RBFN2/" + str(rs.numfeats) + "feats/CoordHitTargetBIN" 
    name = cmaesPath + "/ResCma" + str(sizeT) + "/ResTry1/CoordHitTargetCmaBIN"
    data = fr.getobjread(name)
    tab = []
    for el in data.values():
        for el1 in el:
            tab.append(el1)
    tabx, taby = [], []
    for el in tab:
        tabx.append(el[0])
        taby.append(rs.targetOrdinate)
    plt.figure()
    plt.plot([-0.12, 0.12], [rs.targetOrdinate, rs.targetOrdinate], c = 'r')
    plt.scatter([-rs.sizeOfTarget[0]/2, rs.sizeOfTarget[0]/2], [rs.targetOrdinate, rs.targetOrdinate], marker=u'|', s = 100)
    plt.scatter(tabx, taby, c = 'b')
    plt.show(block = True)

def plotRBFNCostMap():
    fr, rs = initFRRS()
    x0, y0, z = [], [], []
    xt = 0
    name = "RBFN2/" + str(rs.numfeats) + "feats/ResultShuffle/actiMuscuRBFN" + str(rs.sizeOfTarget[3]) + "BIN"
    #example : name = "/home/beucher/Desktop/runRBFN/RBFN/RBFN2/4feats/Res42/actiMuscuRBFN0.1BIN"
    data = fr.getobjread(name)
    for key, val in data.items():
        x0.append(float(key.split("//")[0]))
        y0.append(float(key.split("//")[1]))
        z.append(np.mean(val))
    xi = np.linspace(-0.25,0.25,200)
    yi = np.linspace(0.35,0.5,200)
    zi = griddata(x0, y0, z, xi, yi)
    plt.figure()
    t1 = plt.scatter(x0, y0, c=z, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
    plt.colorbar(t1, shrink=0.5, aspect=5)
    plt.show(block = True)

def plotAllCmaes(nameF, rbfn = False):
    fr, rs = initFRRS()
    x0, y0, z = {}, {}, {}
    xt = 0
    zDico = []
    for i in range(len(rs.sizeOfTarget)):
        try:
            if rbfn == False:
                name = cmaesPath + "/ResCma" + str(rs.sizeOfTarget[i]) + "/" + nameF + "/saveMvtCost"
            else:
                name = "RBFN2/" + str(rs.numfeats) + "feats/" + nameF + "/saveMvtCost"
            zDico.append(fr.getobjreadJson(name))
        except:
            pass
 
    for i in range(len(zDico)):
        x0[i], y0[i], z[i] = [], [], []
        for keyu, valu in zDico[i].items():
            x0[i].append(float(keyu.split("//")[0]))    
            y0[i].append(float(keyu.split("//")[1]))   
            z[i].append(np.mean(valu))
        x0[i] = np.asarray(x0[i])
        y0[i] = np.asarray(y0[i])
        z[i] = np.asarray(z[i])
    
    xi = np.linspace(-0.25,0.25,200)
    yi = np.linspace(0.35,0.5,200)
    zi = {}
    for i in range(len(z)):
        zi[i] = griddata(x0[i], y0[i], z[i], xi, yi)
    
    fig = plt.figure(1, figsize=(16,9))

    for j in range(4):
        ax = plt.subplot2grid((2,2), (j/2,j%2))
        t1 = ax.scatter(x0[j], y0[j], c=z[j], marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
        ax.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
        ax.contourf(xi, yi, zi[j], 15, cmap=cm.get_cmap('RdYlBu'))
        fig.colorbar(t1, shrink=0.5, aspect=5)
        ax.set_title(str("CostMap for Target " + str(rs.sizeOfTarget[j])))
    
    plt.show(block = True)
    
def plotTimeDistanceTarget(folderName, rbfn = False):
    fr, rs = initFRRS()
    targetDic = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            targetDic[rs.sizeOfTarget[i]] = getTimeDistance(rs.sizeOfTarget[i], folderName, rbfn)
        except:
            pass
    targetDistTime = []
    for key, val in targetDic.items():
        for el in val:
            targetDistTime.append((key, el[0], el[1]))
    dicoTest, dicoTest2 = {}, {}

    targetDistTimeSorted = sorted(targetDistTime, key = lambda col:(col[0],col[1]))
    for el in targetDistTimeSorted:
        if not el[1] in dicoTest.keys():
            dicoTest[el[1]] = []
        if not el[1] in dicoTest2.keys():
            dicoTest2[el[1]] = []
        dicoTest[el[1]].append(el[0])
        dicoTest2[el[1]].append(el[2])
    plotTab = []

    plt.figure()
    plt.ylabel("time")
    plt.xlabel("size (mm)")
    for key in sorted([x for x in dicoTest.keys()]):
        print(key, dicoTest[key], dicoTest2[key])
        plotTab.append(plt.plot(dicoTest[key], dicoTest2[key], label = str("Distance: " + str(key))))
    plt.legend(loc = 0)
    plt.show(block = True)
            
def plotFittsLaw(folderName, rbfn = False):
    fr, rs = initFRRS()
    data = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            data[rs.sizeOfTarget[i]] = getTimeDistance(rs.sizeOfTarget[i], folderName, rbfn)
        except:
            pass

    timeDistWidth = []
    for key, val in data.items():
        for el in val:
            timeDistWidth.append((el[1], el[0], key))
    MT, DI = [], []
    for el in timeDistWidth:
        MT.append(el[0])
        DI.append(np.log2(el[1]/el[2]))
    slope, intercept, r_value, p_value, std_err = stats.linregress(DI,MT)
    yLR = slope * np.asarray(DI) + intercept
    plt.figure()
    for el in timeDistWidth:
        plt.scatter(np.log2(el[1]/el[2]), el[0])
    plt.plot(DI, yLR)
    plt.title(str("a = " + str(slope) + " b = " + str(intercept)))
    plt.xlabel("log(D/W)/log(2)")
    plt.ylabel("Time")
    plt.show(block = True)
    
def plotPerfSizeDist(folderName, rbfn = False):
    fr, rs = initFRRS()
    sizeDistPerfTmp = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            sizeDistPerfTmp[i] = getDistPerfSize(rs.sizeOfTarget[i], folderName, rbfn)
        except:
            pass
    distDico = {}
    for key, val in sizeDistPerfTmp.items():
        for el in val:
            if not el[1] in distDico.keys():
                distDico[el[1]] = []
            distDico[el[1]].append((el[0], el[2]))
    plotTab = []
    plt.figure()
    plt.ylabel("performance")
    plt.xlabel("size (mm)")
    for key in sorted([x for x in distDico.keys()]):
        plotTab.append(plt.plot([x[0] for x in distDico[key]], [x[1] for x in distDico[key]], label = str("Distance: " + str(key))))
    plt.legend(loc = 0)
    plt.show(block = True)

def plotMapTimeTrajectories(folderName, rbfn = False):
    fr, rs = initFRRS()
    areaTimeBySize = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            areaTimeBySize[rs.sizeOfTarget[i]] = getTimeByArea(rs.sizeOfTarget[i], folderName, rbfn)
        except:
            pass
        
    fig = plt.figure(1, figsize=(16,9))

    for i in range(4):
        x = [x[0] for x in areaTimeBySize[rs.sizeOfTarget[i]]]
        y = [y[1] for y in areaTimeBySize[rs.sizeOfTarget[i]]]
        z = [z[2] for z in areaTimeBySize[rs.sizeOfTarget[i]]]
        xi = np.linspace(-0.25,0.25,200)
        yi = np.linspace(0.35,0.5,200)
        zi = griddata(x, y, z, xi, yi)

        ax = plt.subplot2grid((2,2), (i/2,i%2))
        t1 = ax.scatter(x, y, c=z, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
        ax.scatter(0, rs.targetOrdinate, c ='g', marker='v', s=200)
        ax.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
        fig.colorbar(t1, shrink=0.5, aspect=5)
        ax.set_title(str("TimeMap for Target " + str(rs.sizeOfTarget[i])))
    
    plt.show(block = True)
 
def plotcmaesCostProgress():
    fr, rs = initFRRS()
    costCma = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            name = cmaesPath + "/costEvalAll/costEval" + str(rs.sizeOfTarget[i]) + str(100)
            costCma[str(str(i) + "_" + str(rs.sizeOfTarget[i]))] = fr.getobjread(name)
        except:
            pass
    costEvo = {}
    for key, val in costCma.items():
        costArray = np.asarray(val).reshape(rs.maxIterCmaes, rs.popsizeCmaes)
        costEvo[key] = np.mean(costArray, axis = 1)
    y = []
    for i in range(rs.maxIterCmaes):
        y.append(i)
    f, ax = plt.subplots(len(rs.sizeOfTarget), sharex = True)
    for key, x in costEvo.items():
        ax[int(key.split("_")[0])].plot(y, x)
        ax[int(key.split("_")[0])].set_title(str("Target " + key.split("_")[1]))
    plt.show(block = True)

def plotCostColorMapForAllTheta():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/EvaluationOFTheta/"
    xi = np.linspace(-0.25,0.25,100)
    yi = np.linspace(0.35,0.5,100)
    for el in os.listdir(pathDataFolder + name):
        nameTmp = name + el + "/"
        x0, y0, z = returnX0Y0Z(nameTmp)
        zi = griddata(x0, y0, z, xi, yi)
        fig = plt.figure()
        t1 = plt.scatter(x0, y0, c=z, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
        plt.scatter(0, rs.targetOrdinate, c ='g', marker='v', s=200)
        plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
        fig.colorbar(t1, shrink=0.5, aspect=5)
        plt.show(block = True)
        
def plotTrajWhenTargetNotReach():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/costTrajRBFNBIN"
    data = fr.getobjread(name)
    xr, xnr, yr, ynr = [], [], [], []
    for key, val in data.items():
        if val <= 280:
            xnr.append(float(key.split("//")[0]))
            ynr.append(float(key.split("//")[1]))
        else:
            xr.append(float(key.split("//")[0]))
            yr.append(float(key.split("//")[1]))
    plt.figure()
    plt.scatter(xr, yr, c = 'b')
    plt.scatter(xnr, ynr, c = 'r')
    plt.show(block = True)
   
def plotCostVariation(sizeT):
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/costArrayAll/costArrayBIN" + str(sizeT)
    costArr = fr.getobjread(name)
    print(costArr.shape)
    lineCost = {}
    for i in range(costArr.shape[0]):
        lineCost[i] = costArr.T[i]
    t = []
    for i in range(costArr.shape[0]):
        t.append(i)
    plt.figure()
    for i in range(costArr.shape[0]):
        plt.plot(t, lineCost[i])
        plt.show(block = True)

def plotExperimentSetup():
    fr, rs = initFRRS()
    q1 = np.linspace(-0.6, 2.6, 100, True)
    q2 = np.linspace(-0.2, 3, 100, True)
    posIni = fr.getobjread(rs.experimentFilePosIni)
    xi, yi = [], []
    xb, yb = [0], [0]
    t = 0
    for el in posIni:
        if el[1] == np.min(posIni, axis = 0)[1] and t == 0:
            t += 1
            a, b = mgi(el[0], el[1], 0.3, 0.35)
            a1, b1 = mgd(np.array([[a], [b]]), 0.3, 0.35)
            xb.append(a1[0])
            xb.append(b1[0])
            yb.append(a1[1])
            yb.append(b1[1])
        xi.append(el[0])
        yi.append(el[1])
    pos = []
    for i in range(len(q1)):
        for j in range(len(q2)):
            coordEl, coordHa = mgd(np.array([[q1[i]], [q2[j]]]), 0.3, 0.35)
            pos.append(coordHa)
    x, y = [], []
    for el in pos:
        x.append(el[0])
        y.append(el[1])
    plt.figure()
    plt.scatter(x, y)
    plt.scatter(xi, yi, c = 'r')
    plt.scatter(0, 0.6175, c = "r", marker=u'*', s = 200)
    plt.plot(xb, yb, c = 'r')
    plt.plot([-0.3,0.3], [0.6175, 0.6175], c = 'g')
    plt.show(block = True)

def plotScattergram2(folderName):
    fr, rs = initFRRS()
    data = {}
    for i in range(len(rs.sizeOfTarget)):
        data[rs.sizeOfTarget[i]] = getDataScattergram(rs.sizeOfTarget[i], folderName)
    print(data)
            
    plt.figure(1, figsize=(16,9))

    for i in range(4):
        ax = plt.subplot2grid((2,2), (i/2,i%2))
        ax.hist(data[rs.sizeOfTarget[i]], 20)
        ax.plot([-rs.sizeOfTarget[i], -rs.sizeOfTarget[i]], [0, 20], c = 'r', linewidth = 3)
        ax.plot([rs.sizeOfTarget[i], rs.sizeOfTarget[i]], [0, 20], c = 'r', linewidth = 3)
        ax.set_title(str("HitDispersion for Target " + str(rs.sizeOfTarget[i])))
    
    plt.show(block = True)
        
def plotTrackTraj():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/ResShuffleAll/coordEndEffectorRBFN" + str(rs.sizeOfTarget[3]) + "BIN"
    coordAll = fr.getobjread(name)
    plt.figure()
    for key, val in coordAll.items():
        plt.plot([x[0] for x in val], [y[1] for y in val])
    plt.show(block = True)
    print(len(coordAll))

def plotPlayWithTraj():
    fr, rs = initFRRS()
    data, junk = fr.getInitPos(BrentTrajectoriesFolder)
    x, y, x1, y1 = [], [], [], []
    todel = []
    for key, el in data.items():
        if el[0] > -0.25 and el[0] < 0.2499 and el[1] > 0.271: 
            x.append(el[0])
            y.append(el[1])
        else:
            x1.append(el[0])
            y1.append(el[1])
            todel.append(key)

    print(len(todel), todel)
    print(np.max(x), np.min(x), np.min(y))
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(x1, y1, c = 'r')
    plt.show(block = True)
        
def plotLearningFieldRBFN():
    fr, rs = initFRRS()
    posIni = fr.getobjread(rs.experimentFilePosIni)
    x, y = [], []
    for el in posIni:
        x.append(el[0])
        y.append(el[1])
        
    r, ang = [], []
    for el in posIni:
        a, b = invPosCircle(el[0], el[1])
        a, b = round(a, 2), round(b, 3)
        r.append(a)
        ang.append(b)
    
    xy, junk = fr.getInitPos(BrentTrajectoriesFolder)
    sx, sy = [], []
    for key, val in xy.items():
        rr, tt = invPosCircle(val[0], val[1])
        rr, tt = round(rr, 2), round(tt, 3)
        if rr <= (np.max(r) + (abs(r[1] - r[0]))) and rr >= (np.min(r) - (r[1] - r[0])) and tt >= (np.min(ang) - abs(ang[1] - ang[0])) and tt <= (np.max(ang) + abs(ang[1] - ang[0])):
            sx.append(val[0])
            sy.append(val[1])
        else:
            pass
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(sx, sy, c = 'r')
    plt.show(block = True)

def plotLearningFieldRBFNSquare():
    fr, rs = initFRRS()
    posIni = fr.getobjread(rs.experimentFilePosIni)
    x, y = [], []
    for el in posIni:
        x.append(el[0])
        y.append(el[1])
    xy, junk = fr.getInitPos(BrentTrajectoriesFolder)
    sx, sy = [], []
    for key, val in xy.items():
        if val[0] <= (np.max(x) + 0.02) and val[0] >= (np.min(x) - 0.02) and val[1] >= (np.min(y) - 0.01) and val[1] <= (np.max(y) + 0.02):
            sx.append(val[0])
            sy.append(val[1])
        else:
            pass
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(sx, sy, c = 'r')
    plt.show(block = True)

def plotTimeVariationForEachDistance(sizeTarget):
    fr, rs = initFRRS()
    name = cmaesPath + "/ResCma" + str(sizeTarget) + "/nbItecp5CmaBIN"
    nbIteTraj = fr.getobjread(name)
    distTimeDico = {}
    for key, val in nbIteTraj.items():
        nbIteTraj[key] = int(np.mean(nbIteTraj[key]))
        r, t = invPosCircle(float(key.split("//")[0]), float(key.split("//")[1]))
        r, t = round(r, 2), round(t, 3)
        if not r in distTimeDico.keys():
            distTimeDico[r] = []
        distTimeDico[r].append((nbIteTraj[key], t))
    print(distTimeDico)
    
    plt.figure()
    for key, val in distTimeDico.items():
        for el in val:
            plt.scatter(el[1], el[0])
        break
    plt.show(block = True)

#----------------------------------------------------------------------------------------------------------------------------
#Functions related to velocity profiles
    
def plotVelocityProfileRBFN(sizeT):
    fr, rs = initFRRS()
    #name = "RBFN2/" + str(rs.numfeats) + "feats/SpeedSaveBIN" 
    name = cmaesPath + "/ResCma" + str(sizeT) + "/ResTK2/SpeedSaveCmaBIN"
    nameNbIte = cmaesPath + "/ResCma" + str(sizeT) + "/ResTK2/nbIteCmaBIN"
    data = fr.getobjread(name)
    nbIte = fr.getobjread(nameNbIte)
    aAll, vAll, tAll = {}, {}, {}
    for key, val in data.items():
        a = []
        for i in range(nbIte[key][0]):
            a.append(data[key][i])
        #print(key, len(a), a)
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
    plt.figure()
    for key, val in vAll.items():
        t = plt.plot(tAll[key], val, label=str("Bruit = " + str(rs.knoiseU)))
    plt.xlabel("time")
    plt.ylabel("Instantaneous speed")
    plt.title("Velocity profile")
    plt.show(block = True)

def plotVelocityProfiles(folderName, rbfn = False):
    fr, rs = initFRRS()
    fig = plt.figure(1, figsize=(16,9))

    if rbfn:
        t, v = getVelocityProfileDataRBFN(folderName)
        for key, val in v.items():
            plt.plot(t[key], val, c ='b')
            plt.title("Velocity profiles for RBFN ")
    else:
        for i in range(4):
            ax = plt.subplot2grid((2,2), (i/2,i%2))
            t, v = getVelocityProfileDataCMAES(rs.sizeOfTarget[i], folderName)
            for key, val in v.items():
                ax.plot(t[key], val, c ='b')
                ax.set_title(str("Velocity profiles for target " + str(rs.sizeOfTarget[i])))
    
    plt.show(block = True)

#-----------------------------------------------------------------------------------------
# those functions are not used

def plotInitPos():
    '''
    Plots the initial position of trajectories present in the "trajectoire" directory
    '''
    x0 = []
    y0 = []
    fr, rs = initFRRS()
    xt = 0
    yt = rs.targetOrdinate
    posIni = fr.getobjread(rs.experimentFilePosIni)
    for el in posIni:
        x0.append(el[0])
        y0.append(el[1])
    xy, junk = fr.getInitPos(BrentTrajectoriesFolder)
    x, y = [], []
    aa, keyy = [], []
    for key, el in xy.items():
        x.append(el[0])
        y.append(el[1])
        a = math.sqrt((el[0]**2) + (el[1] - rs.targetOrdinate)**2)
        if tronquerNB(a, 3) not in aa:
            aa.append(tronquerNB(a, 3))
        if a < 0.11:
            keyy.append(key)
        
    plt.figure()
    plt.scatter(x, y, c = "b", marker=u'o', s=10, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)  
    
    plt.show(block = True)

def plotPosTAT(fr, rs):
    xtr, junk = fr.getInitPos(pathDataFolder + "ThetaAllTraj/")
    xt1, yt1 = [], []
    for key, el in xtr.items():
        xt1.append(el[0])
        yt1.append(el[1])
    plt.scatter(xt1, yt1, c = 'y')



def plotInitPosOutputSolver():
    '''
    plots the initial positions of trajectories in output_solver(bin)
    Note: explicit path to be removed
    '''
    angleIni = {}
    Q = []
    name1 = "/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/"
    for el in os.listdir(name1):
        if "brentbvp" in el and not "fail" in el:
            #Chargement du fichier
            mati = np.loadtxt(name1 + el)
            Q.append((el, mati[0,10], mati[0,11]))
            #recuperation de q1 et q2 initiales et conversion en coordonnees
            coordElbow, coordHand = mgd(np.mat([[mati[0,10]], [mati[0,11]]]), 0.3, 0.35)
            angleIni[el] = (coordHand[0], coordHand[1])
    
    angleIni2 = {}  
    name2 = "/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/cluster2/"
    for el in os.listdir(name2):
        if "brentbvp" in el and not "fail" in el:
            #Chargement du fichier
            mati2 = np.loadtxt(name2 + el)
            #Q.append((el, mati[0,10], mati[0,11]))
            #recuperation de q1 et q2 initiales et conversion en coordonnees
            coordElbow2, coordHand2 = mgd(np.mat([[mati2[0,10]], [mati2[0,11]]]), 0.3, 0.35)
            angleIni2[el] = (coordHand2[0], coordHand2[1])
    
    x, y, xy = [], [], []
    for key, el in angleIni.items():
        x.append(el[0])
        y.append(el[1])
        xy.append((key, el[0], el[1]))
        
    x2, y2, xy2 = [], [], []
    for key, el in angleIni2.items():
        x2.append(el[0])
        y2.append(el[1])
        xy2.append((key, el[0], el[1]))
    
    gt = []
    for el in xy2:
        if not el in xy:
            gt.append(el[0])
            
    print(len(gt), gt)
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.show(block = True)

def plotTrajThetaAllTraj():
    '''
    Note: deprecated
    '''
    name = "/home/beucher/workspace/Data/ThetaAllTraj/"
    fr = FileReading()
    traj, junk = fr.getInitPos(name)
    x, y, x1, y1 = [], [], [], []
    for el in traj.values():
        x.append(el[0])
        y.append(el[1])
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.show(block = True)


        
        
