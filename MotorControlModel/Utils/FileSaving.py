#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: FileSaving

Description: Functions to save data into files
'''
import os
import json
import pickle
import numpy as np

def checkIfFolderExists(name):
    if not os.path.isdir(name):
        os.makedirs(name)

def saveTxt(fileName, data):
    '''
    Records data under str format
    
    Input:    -fileName: name of the file where data will be recorded
                -data: recorded data
                
    '''
    print ("txt taille", len(data))
    np.savetxt(fileName, data)
        
def saveStr(fileName, data):
    '''
    Records data under str format
    
    Input:    -fileName: name of the file where data will be recorded
                -data: recorded data
                
    '''
    print ("str taille", len(data))
    with open(fileName, "w") as file:
        file.write(str(data))
    
def saveJson(fileName, data):
    '''
    Records data under Json format
    
    Input:    -fileName: name of the file where data will be recorded
                -data: recorded data
                
    '''
    print ("json taille", len(data))
    f = open(fileName, 'w')
    json.dump(data, f)

def saveBin(fileName, data):
    '''
    Records data under binary format
    
    Input:    -fileName: name of the file where data will be recorded
                -data: recorded data
                
    '''
    print ("taille", len(data))
    with open(fileName, "wb") as file:
        monPickler = pickle.Pickler(file)
        monPickler.dump(data)

def saveAllData(sizeOfTarget, tg, folderName):
    checkIfFolderExists(folderName)
    print("folder Name : ",folderName)
    saveJson(folderName + "saveSpeed", tg.saveSpeed)
    saveJson(folderName + "saveNumberOfIteration", tg.saveNumberOfIteration)
    saveJson(folderName + "saveMvtCost", tg.saveMvtCost)
    for key, val in tg.saveU.items():
        valTmpR = []
        for el in val:
            valTmp = [elt.tolist() for elt in el]
            valTmpR.append(valTmp)
        tg.saveU[key] = valTmpR
    saveJson(folderName + "saveU", tg.saveU)
    saveStr(folderName + "elbowCoord", tg.elbowAllCoord)
    saveStr(folderName + "handCoord", tg.handAllCoord)
    #dispersion, used for scattergram
    saveStr(folderName + "saveCoordEndTraj", tg.saveCoordEndTraj)
        
        
