'''
Author: Thomas Beucher

Module: RunTrajectories

Description: Ce fichier contient les fonctions permettant de lancer la generation des trajectoires
'''
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from Optimisation.costFunction import costFunctionClass
from Utils.ThetaNormalization import vectorToMatrix, unNorm
import matplotlib.pyplot as plt
from Utils.InitUtil import initFRRS
    
def saveDataTrajectories(nameFile, data):
    fileSavingStr(nameFile, data)
    nameFile = nameFile + "BIN"
    fileSavingBin(nameFile, data)
    
def saveAllDataTrajectories(nameSave, sti, meanJu, CorR):
    saveDataTrajectories(nameSave + "CoordTrajectoireELAll" + CorR, sti.save.coordElSave)
    saveDataTrajectories(nameSave + "CoordTrajectoireHAAll" + CorR, sti.save.coordHaSave)
    saveDataTrajectories(nameSave + "Uall" + CorR, sti.Usave)
    saveDataTrajectories(nameSave + "nbIte" + CorR, sti.IteSave)
    saveDataTrajectories(nameSave + "cost" + CorR, meanJu)
    saveDataTrajectories(nameSave + "CoordHitTarget" + CorR, sti.lastCoord)
    saveDataTrajectories(nameSave + "SpeedSave" + CorR, sti.speedSave)
    saveDataTrajectories(nameSave + "costTraj" + CorR, sti.costSave)
 
def runGenTraj():
    fr, rs = initFRRS()
    cf = costFunctionClass()
    nameT = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread(nameT + "ThetaX0BIN")
    sti, meanJu = cf.costFunctionRBFN(theta)
    saveAllDataTrajectories(nameT, sti, meanJu, "RBFN")
    print(meanJu)
    print("Fin de generation de trajectoire!")
    
def getThetaCma(fr, name):
    theta = fr.getobjread(name)
    theta = vectorToMatrix(theta)
    theta = unNorm(theta)
    return theta
    
def runGenTrajCma():
    fr, rs = initFRRS()
    for i in range(len(rs.sizeOfTarget)):
        print("Trajectories generation for target ", rs.sizeOfTarget[i])
        cf = costFunctionClass(4, rs.sizeOfTarget[i])
        #fileSavingBin("targetSizeTmp", rs.sizeOfTarget[i])
        name = "OptimisationResults/solHome/ResCma" + str(rs.sizeOfTarget[i]) + "/thetaSol" + str(rs.sizeOfTarget[i]) + "BIN"
        theta = getThetaCma(fr, name)
        sti, meanJu = cf.costFunctionRBFN(theta)
        nameSave = "OptimisationResults/solHome/ResCma" + str(rs.sizeOfTarget[i]) + str("/")
        saveAllDataTrajectories(nameSave, sti, meanJu, "Cma")
        print(meanJu)
        sti.initParamTraj()
    
    
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
    
    