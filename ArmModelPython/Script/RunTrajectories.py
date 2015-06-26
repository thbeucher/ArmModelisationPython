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
    saveDataTrajectories(nameSave + "stateAndCommand" + CorR, sti.stateAndCommand)
    saveDataTrajectories(nameSave + "coordEndEffector" + CorR, sti.coordEndEffector)
    saveDataTrajectories(nameSave + "CoordHitTargetKM" + CorR, sti.lastCoordKM)
    saveDataTrajectories(nameSave + "actiMuscuKM" + CorR, sti.actiMuscuSaveKM)
    saveDataTrajectories(nameSave + "SpeedSaveKM" + CorR, sti.speedSaveKM)
 
def runGenTraj():
    fr, rs = initFRRS()
    cf = LaunchTrajectories(4, rs.sizeOfTarget[3])
    nameT = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread(nameT + "ThetaX7BIN")
    #theta = np.loadtxt("/home/beucher/workspace/Data/RBFN2/7feats/ThetaX72")
    sti, meanJu = cf.LaunchTrajectoriesRBFN(theta)
    #saveAllDataTrajectories(nameT + "ResNT/", sti, meanJu, "RBFN" + str(rs.sizeOfTarget[3]))
    print(meanJu)
    print("Fin de generation de trajectoire!")
    
#runGenTraj()

def runTrajTest():
    print("Start trajectories generation !")
    fr, rs = initFRRS()
    cf = LaunchTrajectories(4, rs.sizeOfTarget[3])
    name = "/home/beucher/Desktop/runRBFN/RBFN/RBFN2/4feats/"
    theta = np.loadtxt(name + "ThetaX42")
    sti, meanJu = cf.LaunchTrajectoriesRBFN(theta)
    saveAllDataTrajectories(name + "Res42/", sti, meanJu, "RBFN" + str(rs.sizeOfTarget[3]))
    print("End of generation !")
    
#runTrajTest()
    
def getThetaCma(fr, name):
    theta = fr.getobjread(name)
    theta = vectorToMatrix(theta)
    theta = unNorm(theta)
    return theta
    
def runGenTrajCma():
    fr, rs = initFRRS()
    for i in range(len(rs.sizeOfTarget)):
        #try:
        print("Trajectories generation for target ", rs.sizeOfTarget[i])
        cf = LaunchTrajectories(4, rs.sizeOfTarget[i])
        #fileSavingBin("targetSizeTmp", rs.sizeOfTarget[i])
        name = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/thetaSolCma" + str(rs.sizeOfTarget[i]) + "optiTry1BIN"
        theta = getThetaCma(fr, name)
        sti, meanJu = cf.LaunchTrajectoriesRBFN(theta)
        nameSave = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/ResTry1KM/"
        saveAllDataTrajectories(nameSave, sti, meanJu, "Cma")
        print(meanJu)
        sti.initParamTraj()
        #except:
            #pass

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
    saveDataTrajectories(nameSave + "hitDispersion" + pt, sti.lastCoordKM)

def runTrajForScattergram():
    fr, rs = initFRRS()
    posIni = fr.getobjread(rs.experimentFilePosIni)
    for i in range(len(rs.sizeOfTarget)):
        print("Trajectories generation for target ", rs.sizeOfTarget[i])
        name = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/thetaSolCma" + str(rs.sizeOfTarget[i]) + "try1BIN"
        theta = getThetaCma(fr, name)
        xi, yi = 0.1, 0.4175
        pt = str(xi) + "_" + str(yi)
        posIni = fr.getobjread(rs.experimentFilePosIni)
        '''plt.figure()
        plt.scatter(xi, yi, c = 'r')
        plt.scatter([x[0] for x in posIni], [x[1] for x in posIni], c = 'b')
        plt.show()'''
        sti = GenerateTrajectory(4, rs.sizeOfTarget[i])
        sti.setTheta(theta)
        for j in range(100):
            for el in posIni:
                sti.generateTrajectories(el[0], el[1])
        nameSave = "OptimisationResults/ResCma" + str(rs.sizeOfTarget[i]) + "/ResTry1KM/"
        saveHitDisp(nameSave, sti, "All")
        sti.initSaveData()
    print("End of generation !")
        
#runTrajForScattergram()

    
    
