#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: MuscularActivationsPlotFunctions

Description: some plotting functions related to muscular activations
'''

import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
from matplotlib import cm

from Utils.ReadSetupFile import ReadSetupFile
from Utils.FileReading import getobjreadJson, getobjread

def plotMuscularActivations(folderName, rbfn = False):
    '''
    plots the muscular actuations from a folder
    
    input:    -folderName: the folder where the data lies
              -rbfn: get them from rbfn or from cmaes controllers (default is cmaes)

    Note : does not work for the Brent controller
    Note : for CMAES, the target size should be read from the setup file (here, set to 0.1)
    '''
    rs = ReadSetupFile()
    if rbfn == False:
        name = rs.CMAESpath + "0.1/" + folderName + "/saveU"
    else:
        name = rs.RBFNpath + folderName + "/saveU"
    data = getobjreadJson(name)
    u1, u2, u3, u4, u5, u6 = [], [], [], [], [], []
    t = []
    for key, val in data.items():
        for el1 in val:
            for el in el1:
                u1.append(el[0])
                u2.append(el[1])
                u3.append(el[2])
                u4.append(el[3])
                u5.append(el[4])
                u6.append(el[5])
            for i in range(len(el1)):
                t.append(i)
            plt.figure()
            plt.plot(t, u1)
            plt.plot(t, u2)
            plt.plot(t, u3)
            plt.plot(t, u4)
            plt.plot(t, u5)
            plt.plot(t, u6)
            plt.show(block = True)
        break


def plotMuscularActivation(what):
    '''
    plots the muscular actuations from trajectories 
    
    input:    -what: chosen data
              -nbfeat: number of features used to generate the current controller 
    Note : probably deprecated               
    '''
    rs = ReadSetupFile()
    if what == "brent":
        state, command = fr.getStateAndCommandDataFromBrent(BrentTrajectoriesFolder)
        y = {}
        for key, val in command.items():
            y[key] = []
            for i in range(len(val)):
                y[key].append(i)
            plt.figure()
            for i in range(6):
                plt.plot(y[key], np.array(val).T[i])
            plt.show(block = True)
        
    elif what == "rbfn":
        nameR = rs.RBFNpath + "Uall"
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
        name = rs.CMAESpath
#unfinished function???           
    
def plotActiMuscuBrent():
    ''' 
    Plots the muscular activation using the Brent controller
    Note : probably deprecated, the given path is not correct              
    '''
    rs = ReadSetupFile()
    data = getobjread("trajectoires_cout/actiMuscuBIN")
    xi, yi = np.linspace(-0.25,0.25,200), np.linspace(0.26,0.6,200)
    x0, y0, z = [], [], []
    for key, val in data.items():
        x0.append(float(key.split("//")[0]))
        y0.append(float(key.split("//")[1]))
        z.append(val)
    zi = griddata(x0, y0, z, xi, yi)
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=z, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(0, rs.targetOrdinate, c ='g', marker='v', s=200)
    plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
    plt.colorbar(t1, shrink=0.5, aspect=5)
    plt.show(block = True)
