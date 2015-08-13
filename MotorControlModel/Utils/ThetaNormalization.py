#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: Functions

Description: On retrouve dans ce fichier les fonctions pour normaliser theta
'''

import numpy as np
from Utils.FileSaving import saveBin
from GlobalVariables import pathDataFolder, cmaesPath    
    
def normalization(theta):
    maxT = np.max(np.abs(theta), axis = 0)
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] / maxT[i]
    saveBin(str(cmaesPath + "/maxTBIN"), maxT)
    return theta

def normalizationNP(theta):
    maxT = np.max(np.abs(theta), axis = 0)
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] / maxT[i]
    np.savetxt(pathDataFolder + 'inputMaxTmp', maxT)
    return theta

def normalizationNPWithoutSaving(theta):
    maxT = np.loadtxt(pathDataFolder + 'inputMaxTmp')
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] / maxT[i]
    return theta

def unNorm(theta):
    maxT = getobjread(str(cmaesPath + "/maxTBIN"))
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] * maxT[i]
    return theta

def unNormNP(theta):
    maxT = np.loadtxt(pathDataFolder + 'inputMaxTmp')
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] * maxT[i]
    return theta

def matrixToVector(theta):
    thetaTmpN = theta[0]
    for i in range(theta.shape[0]-1):
        thetaTmpN = np.hstack((thetaTmpN, theta[i+1]))
    return thetaTmpN

def vectorToMatrix(theta):
    nb = 0
    for i in range(int(theta.shape[0]/6)):
        thetaTmp = []
        for j in range(6):
            thetaTmp.append(theta[j + nb])
        if i == 0:
            thetaf = np.array([thetaTmp])
        else:
            thetaf = np.vstack((thetaf, np.array([thetaTmp])))
        nb += 6
    theta = thetaf
    return theta
