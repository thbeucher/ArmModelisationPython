import cma
from FileProcessing.FileReading import FileReading
import time
from FileProcessing.FileSaving import fileSavingStr
from Optimisation.costFunction import costFunction
import numpy as np


cf = costFunction()
print("Debut du traitement d'optimisation!")
t0 = time.time()
fr = FileReading()
#Récupération des theta
theta = fr.getobjread("RBFN2/2feats/ThetaBIN")
#Mise sous forme de vecteur simple
thetaTmp = theta[0]
for i in range(theta.shape[0]-1):
    thetaTmp = np.hstack((thetaTmp, theta[i+1]))
resSO = cma.fmin(cf.costFunctionRBFN2, thetaTmp, 0.5)
t1 = time.time()
print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
#print(resSO[0])


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



