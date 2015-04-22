'''
Author: Thomas Beucher

Module: RunTrajectories

Description: Ce fichier contient les fonctions permettant de lancer la generation des trajectoires
'''
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from Optimisation.costFunction import costFunctionRBFN
from Utils.ThetaNormalization import vectorToMatrix, unNorm
import matplotlib.pyplot as plt
from Utils.InitUtil import initFRRS
    
    
def runGenTraj():
    fr, rs = initFRRS()
    print("(0: nothing / 1: CoordTraj / 2: U / 3: nbIte / 4: cost / 5: lastCoord / 6: speed)")
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
        fileSavingBin(nameT + "nbIteBIN", sti.IteSave)
    elif sauv == 4:
        fileSavingStr(nameT + "cost", meanJu)
        fileSavingBin(nameT + "costBIN", meanJu)
    elif sauv == 5:
        fileSavingStr(nameT + "CoordHitTarget", sti.lastCoord)
        fileSavingBin(nameT + "CoordHitTargetBIN", sti.lastCoord)
    elif sauv == 6:
        fileSavingStr(nameT + "SpeedSave", sti.speedSave)
        fileSavingBin(nameT + "SpeedSaveBIN", sti.speedSave)
    print(meanJu)
    print("Fin de generation de trajectoire!")
    
    
def runGenTrajCma():
    fr, rs = initFRRS()
    print("(0: nothing / 1: CoordTraj / 2: U / 3: nbIte / 4: cost / 5: lastCoord / 6: speed)")
    sauv = input("voulez vous sauvegarder les trajectoires: ")
    sauv = int(sauv)
    nameT = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread("OptimisationResults/thetaSolBIN")
    theta = unNorm(theta)
    theta = vectorToMatrix(theta)
    testju, sti, meanJu = costFunctionRBFN(theta)
    if sauv == 1:
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireELAllCma", sti.save.coordElSave)
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireHAAllCma", sti.save.coordHaSave)
    elif sauv == 2:
        fileSavingBin(nameT + "UallCma", sti.Usave)
    elif sauv == 3:
        fileSavingStr(nameT + "nbIteCma", sti.IteSave)
        fileSavingBin(nameT + "nbIteCmaBIN", sti.IteSave)
    elif sauv == 4:
        fileSavingStr(nameT + "costCma", meanJu)
        fileSavingBin(nameT + "costBINCma", meanJu)
    elif sauv == 5:
        fileSavingStr(nameT + "CoordHitTargetCma", sti.lastCoord)
        fileSavingBin(nameT + "CoordHitTargetCmaBIN", sti.lastCoord)
    elif sauv == 6:
        fileSavingStr(nameT + "SpeedSaveCma", sti.speedSave)
        fileSavingBin(nameT + "SpeedSaveCmaBIN", sti.speedSave)
    
    
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
    
    