'''
Author: Thomas Beucher
Module: Cmaes
'''
import cma
from FileProcessing.FileReading import FileReading
import time
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
from Optimisation.costFunction import costFunction
import numpy as np
from FileProcessing.Functions import normalization

def runCmaes(nbfeat):
    cf = costFunction(nbfeat)
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
    resSO = cma.fmin(cf.costFunctionCMAES, thetaTmpN, 1, options={'maxiter':5, 'popsize':10})#Avec theta normalise
    t1 = time.time()
    print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
    #Sauvegarde des solutions de cmaes
    fileSavingStr("OptimisationResults/thetaSol", resSO[0])
    fileSavingBin("OptimisationResults/thetaSolBIN", resSO[0])
    fileSavingStr("OptimisationResults/CmaesRes", resSO)
    fileSavingBin("OptimisationResults/CmaesResBIN", resSO)
    


'''cf = costFunction()
print("Debut du traitement d'optimisation!")
t0 = time.time()
fr = FileReading()
fr.getTheta(3, 0)
thetaNorm = {}
for i in range(6):
    name = "ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)
    thetaNorm[i] = fr.getobjread(name)
thetaN = np.array(thetaNorm[0])
theta = np.array(fr.theta_store["u1"])
for i in range(5):
    theta = np.hstack((theta, fr.theta_store[str("u" + str(i+2))]))
    thetaN = np.hstack((thetaN, thetaNorm[i+1]))
#resSO = cma.fmin(costFunctionTest, thetaN, 0.5)
#resSO = cma.fmin(cf.costFunctionRBFN2, theta, 0.5)
#resSO = cma.fmin(cf.costFunctionTest2, thetaN, 0.5, options={'popsize':5})
#resSO = cma.fmin(cf.costFunctionRBFN2, thetaa, 3)
#print(resSO[0])
t1 = time.time()
print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
#print(resSO[0])'''



