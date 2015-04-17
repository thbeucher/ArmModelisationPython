'''
Author: Thomas Beucher

Module: RunTrajectories

Description: Ce fichier contient les fonctions permettant de lancer la generation des trajectoires
'''
from Utils.FileReading import FileReading
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from Utils.ReadSetupFile import ReadSetupFile
from Optimisation.costFunction import costFunctionRBFN
from Utils.ThetaNormalization import vectorToMatrix
import matplotlib.pyplot as plt
    
    
def runGenTraj():
    fr = FileReading()
    rs = ReadSetupFile()
    print("(0: nothing / 1: CoordTraj / 2: U / 3: nbIte, 4: cost)")
    sauv = input("voulez vous sauvegarder les trajectoires: ")
    sauv = int(sauv)
    nameT = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread(nameT + "ThetaXBIN")
    testju, sti, meanJu = costFunctionRBFN(theta)
    if sauv == 1:
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireELAll", sti.save.coordElSave)
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireHAAll", sti.save.coordHaSave)
    elif sauv == 2:
        fileSavingBin(nameT + "Uall", sti.Usave)
    elif sauv == 3:
        fileSavingStr(nameT + "nbIte", sti.IteSave)
    elif sauv == 4:
        fileSavingStr(nameT + "cost", testju)
        fileSavingBin(nameT + "costBIN", testju)
    print(sti.IteSave)
    print("mean", meanJu)
    print(testju)  
    
    
def runGenTrajCma():
    fr = FileReading()
    rs = ReadSetupFile()
    print("(0: nothing / 1: CoordTraj / 2: U / 3: nbIte, 4: cost)")
    sauv = input("voulez vous sauvegarder les trajectoires: ")
    sauv = int(sauv)
    nameT = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread("OptimisationResults/thetaSolBIN")
    theta = vectorToMatrix(theta)
    testju, sti = costFunctionRBFN(theta)
    if sauv == 1:
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireELAllCma", sti.save.coordElSave)
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireHAAllCma", sti.save.coordHaSave)
    elif sauv == 2:
        fileSavingBin(nameT + "UallCma", sti.Usave)
    elif sauv == 3:
        fileSavingStr(nameT + "nbIteCma", sti.IteSave)
    elif sauv == 4:
        fileSavingStr(nameT + "costCma", testju)
        fileSavingBin(nameT + "costBINCma", testju)
    print(testju)  
    
    
def plotTargetUnreach(sti):
    x0, y0 = [], []
    posini, junk = sti.fr.recup_pos_ini(sti.rs.pathFolderTrajectories)
    for el in posini.values():
        x0.append(el[0])
        y0.append(el[1])
    x, y = [], []
    for el1, el2 in sti.IteSave.items():
        if el2[0] == 400:
            x.append((el1.split("//"))[0])
            y.append((el1.split("//"))[1])
    plt.figure()
    plt.scatter(x0, y0, c = 'b')
    plt.scatter(x, y, c = 'r')
    plt.show(block = True)
    
    