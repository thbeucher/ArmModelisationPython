#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: FileSaving

Description: On retrouve dans ce fichier les fonctions permettant de sauvegarder les donnees du projet
'''
import pickle
from GlobalVariables import pathDataFolder, cmaesPath
import json
import os
        
def fileSavingStr(nameFile, data, loc = 0):
    '''
    Records data under str format
    
    Entrees:    -nameFile: nom du fichier ou enregistrer les donnees
                -data: donnees a enregistrer
                
    '''
    if loc == 0:
        nameToSave = pathDataFolder + nameFile
    else:
        nameToSave = nameFile
    with open(nameToSave, "w") as file:
        file.write(str(data))

def fileSavingBin(nameFile, data, loc = 0):
    '''
    Records data under binary format
    
    Entrees:    -nameFile: nom du fichier ou enregistrer les donnees
                -data: donnees a enregistrer
                
    '''
    if loc == 0:
        nameToSave = pathDataFolder + nameFile
    else:
        nameToSave = nameFile
    with open(nameToSave, "wb") as file:
        monPickler = pickle.Pickler(file)
        monPickler.dump(data)

def fileSavingData(nameFile, data):
    fileSavingStr(nameFile, data)
    nameFile = nameFile + "BIN"
    fileSavingBin(nameFile, data)
    
def fileSavingDataJson(name, data):
    fileSavingStrJson(name, data)

def fileSavingCMAESData(sizeOfTarget, tg):
    nameSave = cmaesPath + "/ResCma" + str(sizeOfTarget) + "/ResUKF1B/"
    fileSavingData(nameSave + "saveNumberOfIteration", tg.saveNumberOfIteration)
    fileSavingData(nameSave + "saveCoordEndTraj", tg.saveCoordEndTraj)
    fileSavingData(nameSave + "saveMvtCost", tg.saveMvtCost)
    fileSavingData(nameSave + "saveSpeed", tg.saveSpeed)
    
def checkFolderExists(name):
    name = pathDataFolder + name
    if not os.path.isdir(name):
        os.makedirs(name)
        
def fileSavingScattergramJson(sizeOfTarget, tg, folderName):
    nameSave = cmaesPath + "/ResCma" + str(sizeOfTarget) + "/" + folderName + "/"
    fileSavingDataJson(nameSave + "hitDispersion", tg.saveCoordEndTraj)
    
def fileSavingAllDataJson(sizeOfTarget, tg, folderName, rbfn = False):
    if rbfn == True:
        nameSave = "RBFN2/" + str(tg.rs.numfeats) + "feats/" + folderName + "/"
    else:
        nameSave = cmaesPath + "/ResCma" + str(sizeOfTarget) + "/" + folderName + "/"
    checkIfFolderExist(nameSave)
    fileSavingDataJson(nameSave + "saveNumberOfIteration", tg.saveNumberOfIteration)
    fileSavingDataJson(nameSave + "saveCoordEndTraj", tg.saveCoordEndTraj)
    fileSavingDataJson(nameSave + "saveMvtCost", tg.saveMvtCost)
    fileSavingDataJson(nameSave + "saveSpeed", tg.saveSpeed)
    fileSavingDataJson(nameSave + "elbowCoord", tg.elbowAllCoord)
    fileSavingDataJson(nameSave + "handCoord", tg.handAllCoord)
    for key, val in tg.saveU.items():
        valTmpR = []
        for el in val:
            valTmp = [elt.tolist() for elt in el]
            valTmpR.append(valTmp)
        tg.saveU[key] = valTmpR
    fileSavingDataJson(nameSave + "saveU", tg.saveU)
    
def fileSavingStrJson(name, data):
    name = pathDataFolder + name
    f = open(name, 'w')
    json.dump(data, f)
        
        
        
