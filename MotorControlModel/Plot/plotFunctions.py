#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: plotFunctions

Description: some plotting functions
'''
import os
import random as rd
import math
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
from matplotlib.mlab import griddata

from Utils.FileReading import getStateData, getXYHandData, getXYElbowData, getCommandData, getInitPos
from Utils.ReadSetupFile import ReadSetupFile
from Utils.NiemRoot import tronquerNB

from Utils.UsefulFunctions import getTimeDistance, getDistPerfSize, getTimeByArea, getDataScattergram, returnDifCost

from ArmModel.Arm import Arm

from GlobalVariables import BrentTrajectoriesFolder, pathDataFolder

#--------------------------- trajectory animations ---------------------------------------------------------------------------------------------

def trajectoriesAnimation(what, folderName = "None", targetSize = "0.1"):
    rs = ReadSetupFile()
    if what == "CMAES":
        name = rs.CMAESpath + targetSize + folderName + "/Log/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Log/"

    ec = getXYElbowData(name)
    hc = getXYHandData(name)
    
    posIni = np.loadtxt(pathDataFolder + rs.experimentFilePosIni)
    
    xEl, yEl, xHa, yHa = [], [], [], []
    for key, val in ec.items():
        for el in val:
            xEl.append(el[0])
            yEl.append(el[1])
        for elhc in hc[key]:
            xHa.append(elhc[0])
            yHa.append(elhc[1])
    
    fig = plt.figure()
    upperArm, = plt.plot([],[]) 
    foreArm, = plt.plot([],[])
    plt.xlim(-0.7, 0.7)
    plt.ylim(-0.7,0.7)
    plt.plot([-0.7,0.7], [rs.YTarget, rs.YTarget])
    plt.scatter([-rs.sizeOfTarget[3]/2, rs.sizeOfTarget[3]/2], [rs.YTarget, rs.YTarget], c ='g', marker='o', s=50)
    plt.scatter([el[0] for el in posIni],[el[1] for el in posIni], c='b')
    
    def init():
        upperArm.set_data([0], [0])
        foreArm.set_data([xEl[0]], [yEl[0]])
        return upperArm, foreArm
    
    def animate(i):
        xe = (0, xEl[i])
        ye = (0, yEl[i])
        xh = (xEl[i], xHa[i])
        yh = (yEl[i], yHa[i])
        upperArm.set_data(xe, ye)
        foreArm.set_data(xh, yh)
        return upperArm, foreArm
    
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(xEl), blit=True, interval=20, repeat=True)
    plt.show(block = True)

#----------------------------------------------------------------------------------------------------------------------------
#Functions related to velocity profiles

def plotVelocityProfile(what, folderName = "None"):
    rs = ReadSetupFile()
    plt.figure(1, figsize=(16,9))

    if what == "CMAES":
        for i in range(4):
            ax = plt.subplot2grid((2,2), (i/2,i%2))
            name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + foldername + "/Log"
            state = getStateData(name)
            for k,v in state.items():
                index, speed = [], []
                for j in range(len(v)):
                    index.append(j)
                    speed.append(np.linalg.norm([v[j][0],v[j][1]]))
                ax.plot(index, speed, c ='b')
                ax.set_xlabel("time")
                ax.set_ylabel("Instantaneous velocity")
                ax.set_title(str("Velocity profiles for target " + str(rs.sizeOfTarget[i])))
    else:
        if what == "Brent":
            name = BrentTrajectoriesFolder
        else:
            name = rs.RBFNpath + folderName + "/Log/"

        state = getStateData(name)
        for k,v in state.items():
            if rd.random()<0.06:
                index, speed = [], []
                for j in range(len(v)):
                    index.append(j)
                    speed.append(np.linalg.norm([v[j][0],v[j][1]]))
                    plt.plot(index, speed, c ='b')
        plt.xlabel("time")
        plt.ylabel("Instantaneous velocity")
        plt.title("Velocity profiles for" + what)
    plt.show(block = True)

def plotXYPositions(what, folderName = "None", targetSize = "0.1"):
    rs = ReadSetupFile()
    plt.figure(1, figsize=(16,9))

    if what == "CMAES":
        name = rs.CMAESpath + targetSize + folderName + "/Log/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Log/"

    state = getXYHandData(name)
    for k,v in state.items():
#        if rd.random()<0.06:
            posX, posY = [], []
            for j in range(len(v)):
                posX.append(v[j][0])
                posY.append(v[j][1])

            plt.plot(posX,posY, c ='b')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("XY Positions for Brent")

    x0 = []
    y0 = []
    posIni = np.loadtxt(pathDataFolder + rs.experimentFilePosIni)
    for el in posIni:
        x0.append(el[0])
        y0.append(el[1])
    xy = getInitPos(BrentTrajectoriesFolder)
    x, y = [], []
    aa, keyy = [], []
    for key, el in xy.items():
        x.append(el[0])
        y.append(el[1])
        a = math.sqrt((el[0] - rs.XTarget)**2 + (el[1] - rs.YTarget)**2)
        b = tronquerNB(a, 3)
        if b not in aa:
            aa.append(b)
        if a < 0.11: #Note : WTF ???
            keyy.append(key)
        
    plt.scatter(x, y, c = "b", marker=u'o', s=10, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(rs.XTarget, rs.YTarget, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)

    plt.show(block = True)

def plotArticularPositions(what, folderName = "None", targetSize = "0.1"):
    rs = ReadSetupFile()
    plt.figure(1, figsize=(16,9))

    if what == "CMAES":
        name = rs.CMAESpath + targetSize + folderName + "/Log/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Log/"

    state = getStateData(name)

    for k,v in state.items():
        if rd.random()<0.06:
            Q1, Q2 = [], []
            for j in range(len(v)):
                Q1.append(v[j][2])
                Q2.append(v[j][3])
            plt.plot(Q1,Q2, c ='b')
    plt.xlabel("Q1")
    plt.ylabel("Q2")
    plt.title("Articular positions for Brent")
    plt.show(block = True)

def plotMuscularActivations(what, folderName = "None", targetSize = "0.1"):
    '''
    plots the muscular activations from a folder
    
    input:    -folderName: the folder where the data lies
              -what: get from Brent, rbfn or from cmaes controllers

    '''
    rs = ReadSetupFile()
    if what == "CMAES":
        name = rs.CMAESpath + targetSize + folderName + "/Log/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Log/"

    U = getCommandData(name)

    u1, u2, u3, u4, u5, u6 = [], [], [], [], [], []
    t = []
    for key, el1 in U.items():
        for i in range(len(el1)):
            t.append(i)
            u1.append(el1[i][0])
            u2.append(el1[i][1])
            u3.append(el1[i][2])
            u4.append(el1[i][3])
            u5.append(el1[i][4])
            u6.append(el1[i][5])

        plt.figure()
        plt.plot(t, u1)
        plt.plot(t, u2)
        plt.plot(t, u3)
        plt.plot(t, u4)
        plt.plot(t, u5)
        plt.plot(t, u6)
        break
    plt.show(block = True)

def plotInitPos():
    '''
    Plots the initial position of trajectories present in the Brent directory
    '''
    rs = ReadSetupFile()
    x0 = []
    y0 = []
    xt = 0
    yt = rs.YTarget
    posIni = np.loadtxt(pathDataFolder + rs.experimentFilePosIni)
    for el in posIni:
        x0.append(el[0])
        y0.append(el[1])
    xy = getInitPos(BrentTrajectoriesFolder)
    x, y = [], []
    aa, keyy = [], []
    for key, el in xy.items():
        x.append(el[0])
        y.append(el[1])
        a = math.sqrt((el[0] - rs.XTarget)**2 + (el[1] - rs.YTarget)**2)
        b = tronquerNB(a, 3)
        if b not in aa:
            aa.append(b)
        if a < 0.11: #Note : WTF ???
            keyy.append(key)
        
    plt.figure()
    plt.scatter(x, y, c = "b", marker=u'o', s=10, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)  
    
    plt.show(block = True)

#-------------------------- cost maps ----------------------------------------------

def plotCostColorMap(what, folderName = "None", targetSize = "0.1"):
    '''
    Cette fonction permet d'afficher le profil de cout des trajectoires
    
    Entrees:    -nbfeat: nombre de features utilises pour generer le controleur actuel
                -what: choix des donnees a afficher
    '''
    rs = ReadSetupFile()
    if what == "CMAES":
        name = rs.CMAESpath + targetSize + folderName + "/Cost/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Cost/"

    costs = getCostData(name)
    
    x0 = []
    y0 = []
    cost = []

    for k, v in costs.items():
        x0.append(v[0])
        y0.append(v[1])
        cost.append(v[2])

    '''
    posi = getobjread(rs.experimentFilePosIni)
    for el in posi:
        x0.append(el[0])
        y0.append(el[1])

    if what == "rbfn":
        name = rs.RBFNpath
        x0, y0, z = returnX0Y0Z(name)
        
    elif what == "cma":
        name = rs.RBFNpath + "costBINCma"
        z = getobjread(name)
        for i in range(len(z)):
            if z[i] > 0:
                z[i] -= rs.rhoCF
        
    elif wha == "brent":
        data = getobjread("Exp12TrajBrent/trajectoire_coutCoordXBIN")
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
    '''
    zb = cost
    xi = np.linspace(-0.25,0.25,100)
    yi = np.linspace(0.35,0.5,100)
    er = 0
    try:
        zb.shape[1]
    except IndexError:
        er = 1
    except AttributeError:
        er = 1
    if type(zb) == type([]) or er == 1:
        zi = griddata(x0, y0, zb, xi, yi)
    else:
        zi = griddata(x0, y0, zb.T[0], xi, yi)
    
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=zb, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(rs.XTarget, rs.YTarget, c ='g', marker='v', s=200)
    CS = plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t1, shrink=0.5, aspect=5)
    plt.show(block = True)

#-----------------------------------------------------------------------------------------------------------
    
def plotTimeDistanceTarget(folderName, rbfn = False):
    rs = ReadSetupFile()
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
    rs = ReadSetupFile()
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
    rs = ReadSetupFile()
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
    rs = ReadSetupFile()
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
        ax.scatter(rs.XTarget, rs.YTarget, c ='g', marker='v', s=200)
        ax.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
        fig.colorbar(t1, shrink=0.5, aspect=5)
        ax.set_title(str("TimeMap for Target " + str(rs.sizeOfTarget[i])))
    
    plt.show(block = True)
 
# ---------------- hit dispersion ---------------------------------------

def plotHitDispersion(sizeT):
    rs = ReadSetupFile()
    #name = rs.RBFNpath + "CoordHitTargetBIN" 
    name = rs.CMAESpath + str(sizeT) + "/ResTry1/CoordHitTargetCmaBIN"
    data = getobjread(name)
    tab = []
    for el in data.values():
        for el1 in el:
            tab.append(el1)
    tabx, taby = [], []
    for el in tab:
        tabx.append(el[0])
        taby.append(rs.YTarget)
    plt.figure()
    plt.plot([-0.12, 0.12], [rs.YTarget, rs.YTarget], c = 'r')
    plt.scatter([-rs.sizeOfTarget[0]/2, rs.sizeOfTarget[0]/2], [rs.YTarget, rs.YTarget], marker=u'|', s = 100)
    plt.scatter(tabx, taby, c = 'b')
    plt.show(block = True)

def plotScattergram(folderName):
    rs = ReadSetupFile()
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
        
# ---------------- end of hit dispersion ---------------------------------------

# --------------------------------- misc ------------------------------------------------------------

def plotcmaesCostProgress():
    rs = ReadSetupFile()
    costCma = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            name = rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/costEvalAll/costEval" + str(100)
            costCma[str(str(i) + "_" + str(rs.sizeOfTarget[i]))] = getobjread(name)
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
        
def plotTrajWhenTargetNotReach():
    rs = ReadSetupFile()
    name = rs.RBFNpath + "costTrajRBFNBIN"
    data = getobjread(name)
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
    rs = ReadSetupFile()
    name = rs.RBFNpath + "costArrayAll/costArrayBIN" + str(sizeT)
    costArr = getobjread(name)
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
    rs = ReadSetupFile()
    q1 = np.linspace(-0.6, 2.6, 100, True)
    q2 = np.linspace(-0.2, 3, 100, True)
    posIni = getobjread(rs.experimentFilePosIni)
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

def plotTrackTraj():
    rs = ReadSetupFile()
    name = rs.RBFNpath + "ResShuffleAll/coordEndEffectorRBFN" + str(rs.sizeOfTarget[3]) + "BIN"
    coordAll = getobjread(name)
    plt.figure()
    for key, val in coordAll.items():
        plt.plot([x[0] for x in val], [y[1] for y in val])
    plt.show(block = True)
    print(len(coordAll))

def plotPlayWithTraj():
    rs = ReadSetupFile()
    data= getInitPos(BrentTrajectoriesFolder)
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
    rs = ReadSetupFile()
    posIni = getobjread(rs.experimentFilePosIni)
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
    
    xy= getInitPos(BrentTrajectoriesFolder)
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
    rs = ReadSetupFile()
    posIni = getobjread(rs.experimentFilePosIni)
    x, y = [], []
    for el in posIni:
        x.append(el[0])
        y.append(el[1])
    xy= getInitPos(BrentTrajectoriesFolder)
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
    rs = ReadSetupFile()
    name = rs.CMAESpath + str(sizeTarget) + "/nbItecp5CmaBIN"
    nbIteTraj = getobjread(name)
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

#-----------------------------------------------------------------------------------------
# those functions are not used

def plotPosTAT(fr, rs):
    xtr= getInitPos(pathDataFolder + "ThetaAllTraj/")
    xt1, yt1 = [], []
    for key, el in xtr.items():
        xt1.append(el[0])
        yt1.append(el[1])
    plt.scatter(xt1, yt1, c = 'y')



        
        
