#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: Functions

Description: On retrouve dans ce fichier les fonctions pour normaliser theta
'''

import numpy as np
from Utils.FileReading import FileReading
from Utils.FileSaving import fileSavingBin
from GlobalVariables import pathDataFolder
    
    
def normalization(theta):
    maxT = np.max(np.abs(theta), axis = 0)
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] / maxT[i]
    fileSavingBin(str(cmaesPath + "/maxTBIN"), maxT)
    return theta

def unNorm(theta):
    fr = FileReading()
    maxT = fr.getobjread(str(cmaesPath + "/maxTBIN"))
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

def normalizationNP(theta, rs):
    maxT = np.max(np.abs(theta), axis = 0)
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] / maxT[i]
    np.savetxt(pathDataFolder + 'inputMaxTmp', maxT)
    return theta

def normalizationNPWithoutSaving(theta, rs):
    maxT = np.loadtxt(pathDataFolder + 'inputMaxTmp')
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] / maxT[i]
    return theta

def unNormNP(theta, rs):
    maxT = np.loadtxt(pathDataFolder + 'inputMaxTmp')
    for i in range(theta.shape[1]):
        theta[:,i] = theta[:,i] * maxT[i]
    return theta





'''def normalizeThetaFunction():
    fr = FileReading()
    fr.getTheta(3, 0)
    vzeros = []
    #Enregistrement des theta en Str
    for i in range(6):
        name = "ThetaAllTraj/Theta_u" + str(i+1)
        fileSavingStr(name, fr.theta_store[str("u" + str(i+1))])
    #Normalisation des theta
    for i in range(6):
        mini = np.min(fr.theta_store[str("u" + str(i+1))])
        maxi = np.max(fr.theta_store[str("u" + str(i+1))])
        vs = fr.theta_store[str("u" + str(i+1))]
        v = (vs - mini)/(maxi - mini)
        vtest = v + 0.1
        name = "ThetaAllTraj/thetaNormalize_u" + str(i+1)
        fileSavingStr(name, v)
        nameb = "ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)
        fileSavingBin(nameb, v)
    #Coefficient de normalisation
    for i in range(6):
        namec = "ThetaAllTraj/CoefNormalization_theta_u" + str(i+1)
        vTmp = fr.getobjread(str("ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)))
        coef =  np.divide(vTmp, fr.theta_store[str("u" + str(i+1))])
        fileSavingBin(namec, coef)
        fileSavingStr(str(namec + "_str"), coef)
'''




