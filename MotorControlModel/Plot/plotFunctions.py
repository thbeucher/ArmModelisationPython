#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: plotFunctions

Description: some plotting functions
'''
import os
import random as rd
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
from matplotlib.mlab import griddata

from Utils.FileReading import getStateData, getEstimatedStateData, getEstimatedXYHandData, getXYHandData, getXYElbowData, getCommandData, getNoiselessCommandData, getInitPos, getCostData, getTrajTimeData, getTrajTimeData, getLastXData
from Utils.ReadSetupFile import ReadSetupFile
from Utils.NiemRoot import tronquerNB

from ArmModel.Arm import Arm

from GlobalVariables import BrentTrajectoriesFolder, pathDataFolder

#--------------------------- trajectory animations ---------------------------------------------------------------------------------------------

def trajectoriesAnimation(what, folderName = "None", targetSize = "0.05"):
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
            name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + folderName + "/Log/"
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
            if  rd.random()<0.06:#what == "RBFN" or
                index, speed = [], []
                for j in range(len(v)):
                    index.append(j)
                    speed.append(np.linalg.norm([v[j][0],v[j][1]]))
                    plt.plot(index, speed, c ='b')
        plt.xlabel("time")
        plt.ylabel("Instantaneous velocity")
        plt.title("Velocity profiles for " + what)
    plt.show(block = True)

def plotXYPositions(what, folderName = "None", targetSize = "0.05"):
    rs = ReadSetupFile()

    if what == "CMAES":
        name = rs.CMAESpath + targetSize + "/" + folderName + "/Log/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Log/"

    state = getXYHandData(name)
    estimState = getEstimatedXYHandData(name)

    plt.figure(1, figsize=(16,9))
    for k,v in state.items():
        if rd.random()<0.2 or what != "Brent":
            posX, posY = [], []
            for j in range(len(v)):
                posX.append(v[j][0])
                posY.append(v[j][1])

            plt.plot(posX,posY, c ='b')

    '''
    for k,v in estimState.items():
        if rd.random()<0.06 or what != "Brent":
            eX, eY = [], []
            for j in range(len(v)):
                eX.append(v[j][0])
                eY.append(v[j][1])

            plt.plot(eX,eY, c ='r')
    '''

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("XY Positions for " + what)

    makeInitPlot(rs)

    plt.show(block = True)

def plotArticularPositions(what, folderName = "None", targetSize = "0.05"):
    rs = ReadSetupFile()
 
    if what == "CMAES":
        name = rs.CMAESpath + targetSize + "/" + folderName + "/Log/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Log/"

    state = getStateData(name)

    plt.figure(1, figsize=(16,9))
    for k,v in state.items():
        if rd.random()<0.06 or what != "Brent":
            Q1, Q2 = [], []
            for j in range(len(v)):
                Q1.append(v[j][2])
                Q2.append(v[j][3])
            plt.plot(Q1,Q2, c ='b')
    plt.xlabel("Q1")
    plt.ylabel("Q2")
    plt.title("Articular positions for " + what)
    plt.show(block = True)

def plotMuscularActivations(what, folderName = "None", targetSize = "0.05"):
    '''
    plots the muscular activations from a folder
    
    input:    -folderName: the folder where the data lies
              -what: get from Brent, rbfn or from cmaes controllers

    '''
    rs = ReadSetupFile()
    if what == "CMAES":
        name = rs.CMAESpath + targetSize + "/" + folderName + "/Log/"
    elif what == "Brent":
        name = BrentTrajectoriesFolder
    else:
        name = rs.RBFNpath + folderName + "/Log/"

    U = getNoiselessCommandData(name)

    for key, el1 in U.items():
        t = []
        u1, u2, u3, u4, u5, u6 = [], [], [], [], [], []
        if rd.random()<0.01 or what != "Brent":
            for i in range(len(el1)):
                t.append(i)
                u1.append(el1[i][0])
                u2.append(el1[i][1])
                u3.append(el1[i][2])
                u4.append(el1[i][3])
                u5.append(el1[i][4])
                u6.append(el1[i][5])

            plt.figure()
            plt.plot(t, u1, label = "U1")
            plt.plot(t, u2, label = "U2")
            plt.plot(t, u3, label = "U3")
            plt.plot(t, u4, label = "U4")
            plt.plot(t, u5, label = "U5")
            plt.plot(t, u6, label = "U6")
            plt.legend(loc = 0)

            print key
            val = raw_input('1 to see data, anything otherwise: ')
            val = int(val)
            if val == 1:
                print el1
            #plt.clf()

    plt.xlabel("time")
    plt.ylabel("U")
    plt.title("Muscular Activations for " + what)
    plt.show(block = True)

def makeInitPlot(rs):
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
        
    plt.scatter(x, y, c = "b", marker=u'o', s=10, cmap=cm.get_cmap('RdGrBu'))
    plt.scatter(xt, yt, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)  

def plotInitPos():
    '''
    Plots the initial position of trajectories present in the Brent directory
    '''
    plt.figure()
    rs = ReadSetupFile()
    makeInitPlot(rs)
    
    plt.show(block = True)

#-------------------------- cost maps ----------------------------------------------

def plotCostColorMap(what, folderName = "None", targetSize = "All"):
    '''
    Cette fonction permet d'afficher le profil de cout des trajectoires
    
    Entrees:  -what: choix des donnees a afficher
    '''
    rs = ReadSetupFile()
    fig = plt.figure()

    if what == "CMAES" and targetSize == "All":
        for i in range(len(rs.sizeOfTarget)):
            ax = plt.subplot2grid((2,2), (i/2,i%2))
            name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + folderName + "/Cost/"
            costs = getCostData(name)

            x0 = []
            y0 = []
            cost = []

            for k, v in costs.items():
                for j in range(len(v)):
                    x0.append(v[j][0])
                    y0.append(v[j][1])
                    cost.append(v[j][2])

            xi = np.linspace(-0.25,0.25,100)
            yi = np.linspace(0.35,0.5,100)
            zi = griddata(x0, y0, cost, xi, yi)

            t1 = ax.scatter(x0, y0, c=cost, marker=u'o', s=5, cmap=cm.get_cmap('RdGrBu'))
            ax.scatter(rs.XTarget, rs.YTarget, c ='g', marker='v', s=200)
            CS = ax.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdGrBu'))
            t1 = ax.scatter(x0, y0, c='b', marker=u'o', s=20)
            ax.set_title(str("Cost map for target " + str(rs.sizeOfTarget[i])))
            fig.colorbar(t1, shrink=0.5, aspect=5)

    else:
        if what == "CMAES":
            name = rs.CMAESpath + targetSize + "/" + folderName + "/Cost/"
        elif what == "Brent":
            name = BrentTrajectoriesFolder
        else:
            name = rs.RBFNpath + folderName + "/Cost/"

        costs = getCostData(name)
   
        x0 = []
        y0 = []
        cost = []

        for k, v in costs.items():
            for j in range(len(v)):
                x0.append(v[j][0])
                y0.append(v[j][1])
                cost.append(v[j][2])

        xi = np.linspace(-0.25,0.25,100)
        yi = np.linspace(0.35,0.5,100)
        zi = griddata(x0, y0, cost, xi, yi)
    
        t1 = plt.scatter(x0, y0, c=cost, marker=u'o', s=5, cmap=cm.get_cmap('RdGrBu'))
        plt.scatter(rs.XTarget, rs.YTarget, c ='g', marker='v', s=200)
        CS = plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdGrBu'))
        plt.scatter(x0, y0, c='b', marker=u'o', s=20)
        fig.colorbar(t1, shrink=0.5, aspect=5)
        plt.title("Cost map for " + what)

    plt.show(block = True)

#-------------------------- time maps ----------------------------------------------

def plotTimeColorMap(what, folderName = "None", targetSize = "All"):
    '''
    Cette fonction permet d'afficher le profil de temps des trajectoires
    
    Entrees:      -what: choix des donnees a afficher
    '''
    rs = ReadSetupFile()
    fig = plt.figure()

    if what == "CMAES" and targetSize == "All":
        for i in range(len(rs.sizeOfTarget)):
            ax = plt.subplot2grid((2,2), (i/2,i%2))
            name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + folderName + "/TrajTime/"
            times = getTrajTimeData(name)

            x0 = []
            y0 = []
            time = []

            for k, v in times.items():
                for j in range(len(v)):
                    x0.append(v[j][0])
                    y0.append(v[j][1])
                    time.append(v[j][2])

            xi = np.linspace(-0.25,0.25,100)
            yi = np.linspace(0.35,0.5,100)
            zi = griddata(x0, y0, time, xi, yi)

            t1 = ax.scatter(x0, y0, c=time, marker=u'o', s=50, cmap=cm.get_cmap('RdGrBu'))
            ax.scatter(rs.XTarget, rs.YTarget, c ='g', marker='v', s=200)
            CS = ax.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdGrBu'))
            ax.set_title(str("Time map for target " + str(rs.sizeOfTarget[i])))
            fig.colorbar(t1, shrink=0.5, aspect=5)

    else:
        if what == "CMAES":
            name = rs.CMAESpath + targetSize + "/" + folderName + "/TrajTime/"
        elif what == "Brent":
            name = BrentTrajectoriesFolder
        else:
            name = rs.RBFNpath + folderName + "/TrajTime/"

        times = getTrajTimeData(name)
   
        x0 = []
        y0 = []
        time = []

        for k, v in times.items():
            for j in range(len(v)):
                x0.append(v[j][0])
                y0.append(v[j][1])
                time.append(v[j][2])

        xi = np.linspace(-0.25,0.25,100)
        yi = np.linspace(0.35,0.5,100)
        zi = griddata(x0, y0, time, xi, yi)
    
        t1 = plt.scatter(x0, y0, c=time, marker=u'o', s=50, cmap=cm.get_cmap('RdGrBu'))
        plt.scatter(rs.XTarget, rs.YTarget, c ='g', marker='v', s=200)
        CS = plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdGrBu'))
        fig.colorbar(t1, shrink=0.5, aspect=5)

    plt.show(block = True)

#-----------------------------------------------------------------------------------------------------------
    
def plotTimeDistanceTarget(folderName):
    rs = ReadSetupFile()

    dicoTime = {}
 
    for i in range(len(rs.sizeOfTarget)):
        name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + folderName + "/TrajTime/"

        trajTimes = getTrajTimeData(name)

        for k, v in trajTimes.items():
            for j in range(len(v)):
                distance = round(rs.getDistanceToTarget(v[j][0],v[j][1]),2)
                if not distance in dicoTime.keys():
                    dicoTime[distance] = {}
                if not rs.sizeOfTarget[i] in dicoTime[distance].keys():
                    dicoTime[distance][rs.sizeOfTarget[i]] = []
                dicoTime[distance][rs.sizeOfTarget[i]].append(v[j][2])
 
    plotTab = []

    plt.figure()
    plt.ylabel("time")
    plt.xlabel("Target size (mm)")
    for key in sorted(dicoTime.keys()):
        plotTab.append(plt.plot([i for i in sorted(dicoTime[key].keys())], [np.mean(dicoTime[key][i]) for i in sorted(dicoTime[key].keys())], label = str("Distance: " + str(key))))
    plt.legend(loc = 0)
    plt.show(block = True)

#-----------------------------------------------------------------------------------------------------------
    
def plotPerfSizeDist(folderName):
    rs = ReadSetupFile()
    dicoCost = {}
 
    for i in range(len(rs.sizeOfTarget)):
        name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + folderName + "/Cost/"

        costs = getCostData(name)

        for k, v in costs.items():
            for j in range(len(v)):
                distance = round(rs.getDistanceToTarget(v[j][0],v[j][1]),2)
                if not distance in dicoCost.keys():
                    dicoCost[distance] = {}
                if not rs.sizeOfTarget[i] in dicoCost[distance].keys():
                    dicoCost[distance][rs.sizeOfTarget[i]] = []
                dicoCost[distance][rs.sizeOfTarget[i]].append(v[j][2])

    plotTab = []
    plt.figure()
    plt.ylabel("performance")
    plt.xlabel("Target size (mm)")
    for key in sorted(dicoCost.keys()):
        plotTab.append(plt.plot([i for i in sorted(dicoCost[key].keys())], [np.mean(dicoCost[key][i]) for i in sorted(dicoCost[key].keys())], label = str("Distance: " + str(key))))
    plt.legend(loc = 0)
    plt.show(block = True)

#-----------------------------------------------------------------------------------------------------------
            
def plotFittsLaw(folderName, rbfn = False):
    rs = ReadSetupFile()

    timeDistWidth = []
    for i in range(len(rs.sizeOfTarget)):
        name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + folderName + "/TrajTime/"

        trajTimes = getTrajTimeData(name)

        for k, v in trajTimes.items():
            for j in range(len(v)):
                distance = rs.getDistanceToTarget(v[j][0],v[j][1])
                trajtime = v[j][2]
                size = rs.sizeOfTarget[i]
                timeDistWidth.append((distance, size, trajtime))
            
    MT, DI = [], []
    for el in timeDistWidth:
        MT.append(el[2])
        DI.append(np.log2(el[0]/el[1]))
    slope, intercept, r_value, p_value, std_err = stats.linregress(DI,MT)
    yLR = slope * np.asarray(DI) + intercept
    plt.figure()
    for el in timeDistWidth:
        plt.scatter(np.log2(el[0]/el[1]), el[2])
    plt.plot(DI, yLR)
    plt.title(str("a = " + str(slope) + " b = " + str(intercept)))
    plt.xlabel("log(D/W)/log(2)")
    plt.ylabel("Movement time")
    plt.show(block = True)
 
# ---------------- hit dispersion ---------------------------------------

def plotHitDispersion(folderName,sizeT):
    rs = ReadSetupFile()
    name =  rs.CMAESpath + sizeT + "/" + folderName + "/finalX/"
    data = getLastXData(name)

    tabx, taby = [], []
    for el in data.values():
           for j in range(len(el)):
               tabx.append(el[j])
               taby.append(rs.YTarget)

    plt.figure()
    plt.plot([-rs.sizeOfTarget[0]/2, rs.sizeOfTarget[0]/2], [rs.YTarget, rs.YTarget], c = 'r')
    plt.scatter([-rs.sizeOfTarget[0]/2, rs.sizeOfTarget[0]/2], [rs.YTarget, rs.YTarget], marker=u'|', s = 100)
    plt.scatter(tabx, taby, c = 'b')
    plt.show(block = True)

def plotScattergram(what,folderName):
    rs = ReadSetupFile()
    data = {}

    if what=="CMAES":
        for i in range(len(rs.sizeOfTarget)):
            name =  rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/" + folderName + "/finalX/"
            tmp = getLastXData(name)
            tabx = []
            for el in tmp.values():
                for j in range(len(el)):
                    tabx.append(el[j])

                    data[rs.sizeOfTarget[i]] = tabx

        plt.figure(1, figsize=(16,9))

        for i in range(len(rs.sizeOfTarget)):
            ax = plt.subplot2grid((2,2), (i/2,i%2))
            ax.hist(data[rs.sizeOfTarget[i]], 20)
            ax.plot([-rs.sizeOfTarget[i], -rs.sizeOfTarget[i]], [0, 20], c = 'r', linewidth = 3)
            ax.plot([rs.sizeOfTarget[i], rs.sizeOfTarget[i]], [0, 20], c = 'r', linewidth = 3)
            ax.set_title(str("Hit Dispersion for Target " + str(rs.sizeOfTarget[i])))

    elif what=="RBFN":
            name =  rs.RBFNpath + folderName + "/finalX/"
            tmp = getLastXData(name)
            tabx = []
            for el in tmp.values():
                for j in range(len(el)):
                    tabx.append(el[j])
            plt.hist(tabx, 20)
            for i in range(len(rs.sizeOfTarget)):
                plt.plot([-rs.sizeOfTarget[i], -rs.sizeOfTarget[i]], [0, 20], c = 'r', linewidth = 3)
                plt.plot([rs.sizeOfTarget[i], rs.sizeOfTarget[i]], [0, 20], c = 'r', linewidth = 3)
            plt.title("Hit Dispersion for RBFN")
    
    plt.show(block = True)
        
# ---------------- end of hit dispersion ---------------------------------------

def plotCMAESCostProgress():
    rs = ReadSetupFile()

    for i in range(len(rs.sizeOfTarget)):
        ax = plt.subplot2grid((2,2), (i/2,i%2))
        name = rs.CMAESpath + str(rs.sizeOfTarget[i]) + "/Cost/cmaesCost.log"
        data = np.loadtxt(name)

        x,y = [],[]
        for j in range(len(data)):
            x.append(j)
            y.append(data[j])
        ax.plot(x, y)
        ax.set_title(str("Target " + str(rs.sizeOfTarget[i])))

    plt.show(block = True)

def plotExperimentSetup():
    rs = ReadSetupFile()
    arm = Arm()
    q1 = np.linspace(-0.6, 2.6, 100, True)
    q2 = np.linspace(-0.2, 3, 100, True)
    posIni = np.loadtxt(pathDataFolder + rs.experimentFilePosIni)
    xi, yi = [], []
    xb, yb = [0], [0]
    t = 0
    for el in posIni:
        if el[1] == np.min(posIni, axis = 0)[1] and t == 0:
            t += 1
            a, b = arm.mgi(el[0], el[1])
            a1, b1 = arm.mgd(np.array([[a], [b]]))
            xb.append(a1[0])
            xb.append(b1[0])
            yb.append(a1[1])
            yb.append(b1[1])
        xi.append(el[0])
        yi.append(el[1])
    pos = []
    for i in range(len(q1)):
        for j in range(len(q2)):
            coordEl, coordHa = arm.mgd(np.array([[q1[i]], [q2[j]]]))
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
