#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: FileSaving

Description: On retrouve dans ce fichier les fonctions permettant de sauvegarder les donnees du projet
'''
import pickle
from GlobalVariables import pathDataFolder
        
def fileSavingStr(nameFile, data, loc = 0):
    '''
    Cette fonction permet d'enregistrer les donnees sous format str
    
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
    Cette fonction permet d'enregistrer les donnees sous format binaire
    
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

def fileSavingAllData(sizeOfTarget, tg):
    nameSave = "OptimisationResults/ResCma" + str(sizeOfTarget) + "/ResUKF1B/"
    fileSavingData(nameSave + "saveNumberOfIteration", tg.saveNumberOfIteration)
    fileSavingData(nameSave + "saveCoordEndTraj", tg.saveCoordEndTraj)
    fileSavingData(nameSave + "saveMvtCost", tg.saveMvtCost)
    fileSavingData(nameSave + "saveSpeed", tg.saveSpeed)
        
        
        
