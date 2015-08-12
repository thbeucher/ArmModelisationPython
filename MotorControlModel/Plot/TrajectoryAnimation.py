#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: TrajectoryAnimation

Description: We find here functions usefull to run cmaes and latter some script to run trajectories
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from GlobalVariables import pathDataFolder, cmaesPath


# mettre size of target en argument
def trajectoriesAnimation(folderName, rbfn = False):
    rs = ReadSetupFile()
    if rbfn == True:
        nameEC = "RBFN2/" + str(rs.numfeats) + "feats/" + folderName + "/elbowCoord"
        nameHC = "RBFN2/" + str(rs.numfeats) + "feats/" + folderName + "/handCoord"
    else:
        nameEC = cmaesPath + "/ResCma0.005/" + folderName + "/elbowCoord"
        nameHC = cmaesPath + "/ResCma0.005/" + folderName + "/handCoord"
    ec = getobjreadJson(nameEC)
    hc = getobjreadJson(nameHC)
    
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
    plt.plot([-0.7,0.7], [rs.targetOrdinate, rs.targetOrdinate])
    plt.scatter([-rs.sizeOfTarget[3]/2, rs.sizeOfTarget[3]/2], [rs.targetOrdinate, rs.targetOrdinate], c ='g', marker='o', s=50)
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
    
    
    
    
    
