'''
Author: Thomas Beucher

Module: Cmaes

Description: On retrouve dans ce fichier une fonction permettant de lancer l'optimisation stochastique cmaes
'''
import cma
from Utils.FileReading import FileReading
import time
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from Utils.ThetaNormalization import normalization, matrixToVector
from Utils.ReadSetupFile import ReadSetupFile
from Optimisation.costFunction import costFunctionClass
from Utils.NiemRoot import tronquerNB

def runCmaes():
    rs = ReadSetupFile()
    nbfeat = rs.numfeats
    print("Debut du traitement d'optimisation!")
    t0 = time.time()
    fr = FileReading()
    #Récupération des theta
    namec = "RBFN2/" + str(nbfeat) + "feats/ThetaXBIN"
    theta = fr.getobjread(namec)
    maxT, thetaN = normalization(theta)#Recuperation des theta normalises
    fileSavingBin("OptimisationResults/maxTBIN", maxT)
    #Mise sous forme de vecteur simple
    thetaN = matrixToVector(thetaN)
    cf = costFunctionClass()
    resSO = cma.fmin(cf.costFunctionCMAES, thetaN, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
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
    
    
    





