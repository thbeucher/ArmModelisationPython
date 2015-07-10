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
#from matplotlib import animation
#import mpl_toolkits
import os
from ArmModel.GeometricModel import mgd
import math
from Utils.NiemRoot import tronquerNB
from Utils.InitUtil import initFRRS
from Utils.FileReading import FileReading
#from shutil import copyfile
#from posix import remove
from Utils.FunctionsUsefull import returnX0Y0Z, returnDifCostBrentRBFN,\
     getTimeDistance, getDistPerfSize, getVelocityProfileData, getTimeByArea
from matplotlib.mlab import griddata
from scipy.spatial import ConvexHull
from GlobalVariables import pathTrajectoriesFolder, pathDataFolder


def costColorPlot(wha):
    '''
    Cette fonction permet d'afficher le profil de cout des trajectoires
    
    Entrees:    -nbfeat: nombre de features utilises pour generer le controleur actuel
                -wha: choix des donnees a afficher
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
        
    if wha == "rbfn":
        name = "RBFN2/" + str(nbfeat) + "feats/"
        x0, y0, z = returnX0Y0Z(name)
        #maxt = np.max(np.abs(z))
        
    elif wha == "cma":
        name = "RBFN2/" + str(nbfeat) + "feats/costBINCma"
        z = fr.getobjread(name)
        for i in range(len(z)):
            if z[i] > 0:
                z[i] -= rs.rhoCF
        #maxt = np.max(abs(z))
        
    elif wha == "brent":
        data = fr.getobjread("trajectoires_cout/trajectoire_coutCoordXBIN")
        z, x0, y0 = [], [], []
        for el in data:
            z.append(el[1]-rs.rhoCF)
            x0.append(el[2])
            y0.append(el[3])
        #maxt = np.max(np.abs(z))
    
    elif wha == "difBR":
        dif = returnDifCostBrentRBFN()
        z, zobj, x0, y0 = [], [], [], []
        for el in dif:
            if el[2] < 10:
                z.append(el[2])
                zobj.append(el)
                x0.append(el[0])
                y0.append(el[1])
    
    #zb = z/maxt
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


def plotActivationMuscular(what):
    '''
    Cette fonction permet d'afficher les activations musculaires des trajectoires
    
    Entrees:    -wha: choix des donnees a afficher
                -nbfeat: nombre de features utilises pour generer le controleur actuel
                
    '''
    fr, rs = initFRRS()
    nbfeat = rs.numfeats
    if what == "brent":
        state, command = fr.getData(pathTrajectoriesFolder)
        y = {}
        for key, val in command.items():
            y[key] = []
            for i in range(len(command[key])):
                y[key].append(i)
            plt.figure()
            for i in range(6):
                plt.plot(y[key], np.array(command[key]).T[i])
            plt.show(block = True)
        
    elif what == "rbfn":
        nameR = "RBFN2/" + str(nbfeat) + "feats/Uall"
        coutTraj = fr.getobjread(nameR)
        dicoVal = {}
        for key, val in coutTraj.items():
            valu = np.array(val).T
            x = []
            for i in range(valu[0].shape[1]):
                x.append(i)
            rbfn = plt.figure()
            for i in range(valu[0].shape[0]):
                plt.plot(x, valu[0][i])
            plt.show(block = True)
        
    elif what == "cma":
        name = "OptimisationResults/ResCma"
        
        
    
def timeDistance():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/nbIteBIN" 
    data = fr.getobjread(name)
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
    

def hitDispersion(sizeT):
    fr, rs = initFRRS()
    #name = "RBFN2/" + str(rs.numfeats) + "feats/CoordHitTargetBIN" 
    name = "OptimisationResults/ResCma" + str(sizeT) + "/ResTry1/CoordHitTargetCmaBIN"
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
    
#hitDispersion(0.02)
    
def velocityProfile(sizeT):
    fr, rs = initFRRS()
    #name = "RBFN2/" + str(rs.numfeats) + "feats/SpeedSaveBIN" 
    name = "OptimisationResults/ResCma" + str(sizeT) + "/ResTK2/SpeedSaveCmaBIN"
    nameNbIte = "OptimisationResults/ResCma" + str(sizeT) + "/ResTK2/nbIteCmaBIN"
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
    #t = plt.plot(t, v, label=str("Bruit = " + str(rs.knoiseU)))
    plt.xlabel("time")
    plt.ylabel("Instantaneous speed")
    #plt.legend(loc=0)
    plt.title("Velocity profile")
    plt.show(block = True)

#velocityProfile(0.02)

def plotForAllTargetVelocityProfile():
    fr, rs = initFRRS()
    fig = plt.figure(1, figsize=(16,9))
    ax1 = plt.subplot2grid((2,2), (0,0))
    t, v = getVelocityProfileData(rs.sizeOfTarget[0])
    for key, val in v.items():
        ax1.plot(t[key], val, c ='b')
    ax1.set_title(str("Velocity profile for target " + str(rs.sizeOfTarget[0])))
    
    ax2 = plt.subplot2grid((2,2), (0,1))
    t, v = getVelocityProfileData(rs.sizeOfTarget[1])
    for key, val in v.items():
        ax2.plot(t[key], val, c ='b')
    ax2.set_title(str("Velocity profile for target " + str(rs.sizeOfTarget[1])))
    
    ax3 = plt.subplot2grid((2,2), (1,0))
    t, v = getVelocityProfileData(rs.sizeOfTarget[2])
    for key, val in v.items():
        ax3.plot(t[key], val, c ='b')
    ax3.set_title(str("Velocity profile for target " + str(rs.sizeOfTarget[2])))
    
    ax4 = plt.subplot2grid((2,2), (1,1))
    t, v = getVelocityProfileData(rs.sizeOfTarget[3])
    for key, val in v.items():
        ax4.plot(t[key], val, c ='b')
    ax4.set_title(str("Velocity profile for target " + str(rs.sizeOfTarget[3])))
    
    plt.show(block = True)

#plotForAllTargetVelocityProfile()
    

def plot_pos_ini():
    '''
    Cette fonction permet d'afficher les positions initiales des trajectoires
    (trajectoire disponible dans le dossier trajectoire)           
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
    xy, junk = fr.recup_pos_ini(pathTrajectoriesFolder)
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
            #copyfile(rs.pathFolderTrajectories + key, rs.pathFolderData + "ThetaAllTraj/" + key)
            #remove(rs.pathFolderTrajectories + key)
    #print(len(aa), aa)
    #print(len(keyy), sorted(keyy))
    '''q1aw = np.linspace(-0.6, 2.6, 100)
    q2aw = np.linspace(-0.2, 3, 100)
    xawt, yawt, xyawt = [], [], []
    for i in range(len(q1aw)):
        for j in range(len(q2aw)):
            el, ha = mgd(np.array([[q1aw[i]], [q2aw[j]]]), 0.3, 0.35)
            xawt.append(ha[0])
            yawt.append(ha[1])
            xyawt.append((ha[0], ha[1]))
    xyawt = np.asarray(xyawt)
    hull = ConvexHull(xyawt)'''
        
    plt.figure()
    #plt.scatter(xawt, yawt, c = 'g')
    plt.scatter(x, y, c = "b", marker=u'o', s=10, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)  
    
    #plt.figure()
    #plt.plot(xyawt[hull.vertices,0], xyawt[hull.vertices,1])
    
    plt.show(block = True)
   
#plot_pos_ini() 

def plotPosTAT(fr, rs):
    xtr, junk = fr.recup_pos_ini(pathDataFolder + "ThetaAllTraj/")
    xt1, yt1 = [], []
    for key, el in xtr.items():
        xt1.append(el[0])
        yt1.append(el[1])
    plt.scatter(xt1, yt1, c = 'y')



#plot_pos_ini()
#Ce bout de code permet d'afficher les positions initiales des trajectoires dans output_solver(bin)
def plotPosIniOutputSolver():
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
            #copyfile(name2 + el[0], name1 + el[0])
            
    print(len(gt), gt)
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    #plt.scatter(x2, y2, c = 'r')
    plt.show(block = True)
    
#plotPosIniOutputSolver()

def plotTrajThetaAllTraj():
    name = "/home/beucher/workspace/Data/ThetaAllTraj/"
    fr = FileReading()
    traj, junk = fr.recup_pos_ini(name)
    x, y, x1, y1 = [], [], [], []
    for el in traj.values():
        x.append(el[0])
        y.append(el[1])
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.show(block = True)
    
#plotTrajThetaAllTraj()

def plotRBFNCostMap():
    fr, rs = initFRRS()
    x0, y0, z = [], [], []
    xt = 0
    name = "RBFN2/" + str(rs.numfeats) + "feats/ResultShuffle/actiMuscuRBFN" + str(rs.sizeOfTarget[3]) + "BIN"
    #name = "/home/beucher/Desktop/runRBFN/RBFN/RBFN2/4feats/Res42/actiMuscuRBFN0.1BIN"
    #data = fr.getobjread(name, 1)
    data = fr.getobjread(name)
    for key, val in data.items():
        x0.append(float(key.split("//")[0]))
        y0.append(float(key.split("//")[1]))
        z.append(np.mean(val))
    xi = np.linspace(-0.25,0.25,200)
    yi = np.linspace(0.35,0.5,200)
    zi = griddata(x0, y0, z, xi, yi)
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=z, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
    plt.colorbar(t1, shrink=0.5, aspect=5)
    plt.show(block = True)
    
#plotRBFNCostMap()
    

def plotAllCmaes(nameF):
    fr, rs = initFRRS()
    x0, y0, z = {}, {}, {}
    xt = 0
    zDico = []
    for i in range(len(rs.sizeOfTarget)):
        try:
            name = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/ResUKF1B/saveMvtCostBIN"
            #name = "RBFN2/" + str(rs.numfeats) + "feats/actiMuscuRBFN" + str(rs.sizeOfTarget[i]) + "BIN"
            #zDico.append(fr.getobjread(name))
            zDico.append(fr.getobjreadJson(name))
        except:
            pass
    print(zDico)
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
    #fig, (ax1, ax2, ax3, ax4) = plt.subplots(len(rs.sizeOfTarget), sharex = True, sharey = True)
    ax1 = plt.subplot2grid((2,2), (0,0))
    t1 = ax1.scatter(x0[0], y0[0], c=z[0], marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    ax1.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    ax1.contourf(xi, yi, zi[0], 15, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t1, shrink=0.5, aspect=5)
    ax1.set_title(str("CostMap for Target " + str(rs.sizeOfTarget[0])))
    
    ax2 = plt.subplot2grid((2,2), (0,1))
    t2 = ax2.scatter(x0[1], y0[1], c=z[1], marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    ax2.contourf(xi, yi, zi[1], 15, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t2, shrink=0.5, aspect=5)
    ax2.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    ax2.set_title(str("CostMap for Target " + str(rs.sizeOfTarget[1])))
    
    ax3 = plt.subplot2grid((2,2), (1,0))
    t3 = ax3.scatter(x0[2], y0[2], c=z[2], marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t3, shrink=0.5, aspect=5)
    ax3.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    ax3.contourf(xi, yi, zi[2], 15, cmap=cm.get_cmap('RdYlBu'))
    ax3.set_title(str("CostMap for Target " + str(rs.sizeOfTarget[2])))
    
    ax4 = plt.subplot2grid((2,2), (1,1))
    t4 = ax4.scatter(x0[3], y0[3], c=z[3], marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t4, shrink=0.5, aspect=5)
    ax4.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    ax4.contourf(xi, yi, zi[3], 15, cmap=cm.get_cmap('RdYlBu'))
    ax4.set_title(str("CostMap for Target " + str(rs.sizeOfTarget[3])))
    
    plt.show(block = True)
    
#plotAllCmaes()

def plotTimeDistanceTarget(folderName):
    fr, rs = initFRRS()
    targetDic = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            targetDic[rs.sizeOfTarget[i]] = getTimeDistance(rs.sizeOfTarget[i], folderName)
        except:
            pass
    targetDistTime = []
    for key, val in targetDic.items():
        for el in val:
            targetDistTime.append((key, el[0], el[1]))
    dicoTest, dicoTest2 = {}, {}
    print("la", targetDistTime)
    print("sorted", sorted(targetDistTime, key = lambda col:(col[0],col[1])))
    targetDistTimeSorted = sorted(targetDistTime, key = lambda col:(col[0],col[1]))
    for el in targetDistTimeSorted:
        if not el[1] in dicoTest.keys():
            dicoTest[el[1]] = []
        if not el[1] in dicoTest2.keys():
            dicoTest2[el[1]] = []
        dicoTest[el[1]].append(el[0])
        dicoTest2[el[1]].append(el[2])
    plotTab = []
    print(dicoTest)
    print("ici", dicoTest2)
    plt.figure()
    plt.ylabel("time")
    plt.xlabel("size (mm)")
    for key in sorted([x for x in dicoTest.keys()]):
        print(key, dicoTest[key], dicoTest2[key])
        plotTab.append(plt.plot(dicoTest[key], dicoTest2[key], label = str("Distance: " + str(key))))
    plt.legend(loc = 0)
    plt.show(block = True)
            

#plotTimeDistanceTarget()


def plotFittsLaw(folderName):
    fr, rs = initFRRS()
    data = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            data[rs.sizeOfTarget[i]] = getTimeDistance(rs.sizeOfTarget[i], folderName)
        except:
            pass
    print(data)
    timeDistWidth = []
    for key, val in data.items():
        for el in val:
            timeDistWidth.append((el[1], el[0], key))
    print(timeDistWidth)
    MT, DI = [], []
    for el in timeDistWidth:
        MT.append(el[0])
        DI.append(np.log2(el[1]/el[2]))
    slope, intercept, r_value, p_value, std_err = stats.linregress(DI,MT)
    yLR = slope * np.asarray(DI) + intercept
    print(slope, intercept)
    plt.figure()
    for el in timeDistWidth:
        plt.scatter(np.log2(el[1]/el[2]), el[0])
    plt.plot(DI, yLR)
    plt.title(str("a = " + str(slope) + " b = " + str(intercept)))
    plt.xlabel("log(D/W)/log(2)")
    plt.ylabel("Time")
    plt.show(block = True)
    
#plotFittsLaw()
        
def plotPerfSizeDist(folderName):
    fr, rs = initFRRS()
    sizeDistPerfTmp = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            sizeDistPerfTmp[i] = getDistPerfSize(rs.sizeOfTarget[i], folderName)
        except:
            pass
    print(sizeDistPerfTmp)
    distDico = {}
    for key, val in sizeDistPerfTmp.items():
        for el in val:
            if not el[1] in distDico.keys():
                distDico[el[1]] = []
            distDico[el[1]].append((el[0], el[2]))
    print(distDico)
    plotTab = []
    plt.figure()
    plt.ylabel("performance")
    plt.xlabel("size (mm)")
    for key in sorted([x for x in distDico.keys()]):
        plotTab.append(plt.plot([x[0] for x in distDico[key]], [x[1] for x in distDico[key]], label = str("Distance: " + str(key))))
    plt.legend(loc = 0)
    plt.show(block = True)
        
#plotPerfSizeDist()

def plotMapTimeTrajectories():
    fr, rs = initFRRS()
    areaTimeBySize = {}
    for i in range(len(rs.sizeOfTarget)):
        try:
            areaTimeBySize[rs.sizeOfTarget[i]] = getTimeByArea(rs.sizeOfTarget[i])
        except:
            pass
    for key, val in areaTimeBySize.items():
        x = [x[0] for x in val]
        y = [y[1] for y in val]
        z = [z[2] for z in val]
        xi = np.linspace(-0.25,0.25,200)
        yi = np.linspace(0.35,0.5,200)
        zi = griddata(x, y, z, xi, yi)
        fig = plt.figure(1, figsize=(16,9))
        ax1 = plt.subplot2grid((2,2), (0,0))
        t1 = ax1.scatter(x, y, c=z, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
        ax1.scatter(0, rs.targetOrdinate, c ='g', marker='v', s=200)
        ax1.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
        fig.colorbar(t1, shrink=0.5, aspect=5)
        ax1.set_title(str("TimeMap for Target " + str(rs.sizeOfTarget[0])))
        plt.show(block = True)
        
    
#plotMapTimeTrajectories()


        
        
