'''
Author: Thomas Beucher

Module: RunTrajectories

Description: Ce fichier contient les fonctions permettant de lancer la generation des trajectoires
'''
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from Optimisation.LaunchTrajectories import LaunchTrajectories
from Utils.ThetaNormalization import vectorToMatrix, unNorm
import matplotlib.pyplot as plt
from Utils.InitUtil import initFRRS
import math
from Main.GenerateTrajectory import GenerateTrajectory
    
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
    saveDataTrajectories(nameSave + "actiMuscu" + CorR, sti.actiMuscuSave)
 
def runGenTraj():
    fr, rs = initFRRS()
    cf = LaunchTrajectories(4, rs.sizeOfTarget[3])
    nameT = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread(nameT + "ThetaX7BIN")
    sti, meanJu = cf.LaunchTrajectoriesRBFN(theta)
    saveAllDataTrajectories(nameT + "ResShuffleAll/", sti, meanJu, "RBFN" + str(rs.sizeOfTarget[3]))
    print(meanJu)
    print("Fin de generation de trajectoire!")
    
#runGenTraj()
    
def getThetaCma(fr, name):
    theta = fr.getobjread(name)
    theta = vectorToMatrix(theta)
    theta = unNorm(theta)
    return theta
    
def runGenTrajCma():
    fr, rs = initFRRS()
    for i in range(len(rs.sizeOfTarget)):
        print("Trajectories generation for target ", rs.sizeOfTarget[i])
        cf = LaunchTrajectories(4, rs.sizeOfTarget[i])
        #fileSavingBin("targetSizeTmp", rs.sizeOfTarget[i])
        name = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/thetaSol" + str(rs.sizeOfTarget[i]) + "BINcfb"
        theta = getThetaCma(fr, name)
        sti, meanJu = cf.LaunchTrajectoriesRBFN(theta)
        nameSave = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/ResCfb/"
        saveAllDataTrajectories(nameSave, sti, meanJu, "Cma")
        print(meanJu)
        sti.initParamTraj()

#runGenTrajCma()    
    
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
    
def saveHitDisp(nameSave, sti, pt):
    saveDataTrajectories(nameSave + "hitDispersion" + pt, sti.lastCoord)

def runTrajForScattergram():
    fr, rs = initFRRS()
    for i in range(len(rs.sizeOfTarget)):
        print("Trajectories generation for target ", rs.sizeOfTarget[i])
        name = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/thetaSol" + str(rs.sizeOfTarget[i]) + "BINcfb"
        theta = getThetaCma(fr, name)
        xi, yi = -0.05, 0.4175
        pt = str(xi) + "_" + str(yi)
        '''posIni = fr.getobjread(rs.experimentFilePosIni)
        plt.figure()
        plt.scatter(xi, yi, c = 'r')
        plt.scatter([x[0] for x in posIni], [x[1] for x in posIni], c = 'b')
        plt.show()'''
        for i in range(4):
            sti = GenerateTrajectory(4, rs.sizeOfTarget[i])
            for j in range(1000):
                sti.generateTrajectories(xi, yi, theta)
            nameSave = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/ResCfb/"
            saveHitDisp(nameSave, sti, pt)
            sti.initSaveData()
        print("End of generation !")
        
#runTrajForScattergram()

    
    
