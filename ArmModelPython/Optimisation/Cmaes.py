'''
Author: Thomas Beucher

Module: Cmaes

Description: On retrouve dans ce fichier une fonction permettant de lancer l'optimisation stochastique cmaes
'''
import cma
from Utils.FileReading import FileReading
import time
from Utils.FileSaving import fileSavingStr, fileSavingBin
from Optimisation.costFunction import costFunction
import numpy as np
from Utils.ThetaNormalization import normalization
from Utils.ReadSetupFile import ReadSetupFile

def runCmaes(nbfeat):
    cf = costFunction(nbfeat)
    rs = ReadSetupFile()
    rs.readingSetupFile()
    print("Debut du traitement d'optimisation!")
    t0 = time.time()
    fr = FileReading()
    #Récupération des theta
    namec = "RBFN2/" + str(nbfeat) + "feats/ThetaXBIN"
    theta = fr.getobjread(namec)
    maxT, thetaN = normalization(theta)#Recuperation des theta normalises
    fileSavingBin("OptimisationResults/maxTBIN", maxT)
    cf.recupMaxThetaN(maxT)
    #Mise sous forme de vecteur simple
    thetaTmp = theta[0]
    thetaTmpN = thetaN[0]#theta normalise
    for i in range(theta.shape[0]-1):
        thetaTmp = np.hstack((thetaTmp, theta[i+1]))
        thetaTmpN = np.hstack((thetaTmpN, thetaN[i+1]))#theta normalise
    #resSO = cma.fmin(cf.costFunctionCMAES, thetaTmp, 1)
    #resSO = cma.fmin(cf.costFunctionCMAES, thetaTmp, 1, options={'maxiter':5, 'popsize':10})#Avec theta
    resSO = cma.fmin(cf.costFunctionCMAES, thetaTmpN, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})#Avec theta normalise
    t1 = time.time()
    print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
    #Sauvegarde des solutions de cmaes
    fileSavingStr("OptimisationResults/thetaSol", resSO[0])
    fileSavingBin("OptimisationResults/thetaSolBIN", resSO[0])
    fileSavingStr("OptimisationResults/CmaesRes", resSO)
    fileSavingBin("OptimisationResults/CmaesResBIN", resSO)
    






