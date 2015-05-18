'''
Author: Thomas Beucher

Module: Cmaes

Description: On retrouve dans ce fichier une fonction permettant de lancer l'optimisation stochastique cmaes
'''
import cma
import time
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from Utils.ThetaNormalization import normalization, matrixToVector
from Optimisation.LaunchTrajectories import LaunchTrajectories
from Utils.NiemRoot import tronquerNB
from Utils.InitUtil import initFRRS
from Utils.ReadSetupFile import ReadSetupFile
import os
from shutil import copyfile
from multiprocessing.pool import ThreadPool, Pool

def runCmaes():
#Thomas: commenter toutes les méthodes
    fr, rs = initFRRS()
    nbfeat = rs.numfeats
    print("Debut du traitement d'optimisation!")
    t0 = time.time()
    #Récupération des theta
    namec = "RBFN2/" + str(nbfeat) + "feats/ThetaX0BIN"
    theta = fr.getobjread(namec)
    thetaN = normalization(theta)#Recuperation des theta normalises
    #Mise sous forme de vecteur simple
    thetaN = matrixToVector(thetaN)
    cf = LaunchTrajectories()
    resSO = cma.fmin(cf.LaunchTrajectoriesCMAES, thetaN, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    t1 = time.time()
    print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
    #Sauvegarde des solutions de cmaes
    fileSavingStr("OptimisationResults/thetaSol", resSO[0])
    fileSavingBin("OptimisationResults/thetaSolBIN", resSO[0])
    fileSavingStr("OptimisationResults/CmaesRes", resSO)
    fileSavingBin("OptimisationResults/CmaesResBIN", resSO)
    

def unitaryTestCmaes(noise):
    x = np.linspace(0, 100, 10)
    for i in range(x.shape[0]):
        x[i] = tronquerNB(x[i], 3)
    y = x*noise[0] - noise[1]
    z = np.abs(x - y)
    t = np.mean(z)
    return t

'''noise = [10,15]
resT = cma.fmin(unitaryTestCmaes, noise, 10, options={'maxiter':30, 'popsize':50})
print("resultat", resT[0])'''
    
def procUse(sizeT):
    fr, rs = initFRRS()
    nbfeat = rs.numfeats
    print("Debut du traitement d'optimisation! (" + str(sizeT) + ")")
    t0 = time.time()
    #Récupération des theta
    namec = "RBFN2/" + str(nbfeat) + "feats/ThetaX4BIN"
    theta = fr.getobjread(namec)
    thetaN = normalization(theta)#Recuperation des theta normalises
    #Mise sous forme de vecteur simple
    thetaN = matrixToVector(thetaN)
    cf = LaunchTrajectories(4, sizeT)
    
    resSO = cma.fmin(cf.LaunchTrajectoriesCMAES, thetaN, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    
    nameTmp = rs.pathFolderData + "OptimisationResults/ResCma" + str(sizeT)
    if os.path.isdir(nameTmp) == False:
        os.mkdir(nameTmp)
    nameTmp2 = rs.pathFolderProject + "ArmModelPython/Optimisation/"
    for el in os.listdir(nameTmp2):
        if "outcmaes" in el:
            copyfile(nameTmp2 + el, nameTmp + "/" + el)
    
    #Sauvegarde des solutions de cmaes
    nameS = "OptimisationResults/ResCma" + str(sizeT) +"/thetaSol" + str(sizeT)
    nameSB = nameS + "BIN"
    if os.path.isfile(rs.pathFolderData + nameS) == True:
        a = 1
        for el in os.listdir(rs.pathFolderData + "OptimisationResults/ResCma" + str(sizeT) + "/"):
            if "thetaSol" in el:
                a += 1
        nameS += "cp2" + str(a)
        nameSB += "cp2" + str(a)
    fileSavingStr(nameS, resSO[0])
    fileSavingBin(nameSB, resSO[0])
    fileSavingStr("OptimisationResults/CmaesRes" + str(sizeT), resSO)
    fileSavingBin("OptimisationResults/CmaesResBIN" + str(sizeT), resSO)
    t1 = time.time()
    print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
    


def runMultiTargetCmaes():
    rs = ReadSetupFile()
    print("Debut du traitement d'optimisation!")
    t0 = time.time()
    
    p = Pool(processes=4) 
    p.map(procUse, rs.sizeOfTarget)
    '''for i in range(4):
        procUse(rs.sizeOfTarget[i])'''
    '''pool = ThreadPool(4)
    pool.map(procUse, [rs.sizeOfTarget[0], rs.sizeOfTarget[1], rs.sizeOfTarget[2], rs.sizeOfTarget[3]])'''
        
    t1 = time.time()
    print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
    
 

#runMultiTargetCmaes()


