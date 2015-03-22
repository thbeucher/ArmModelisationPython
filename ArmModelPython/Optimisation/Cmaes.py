import cma
from FileProcessing.FileReading import FileReading
import time
from Regression.functionApproximator_LWR import fa_lwr
from FileProcessing.FileSaving import fileSavingStr
from Optimisation.costFunction import costFunction, costFunctionTest
import numpy as np


cf = costFunction()
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
resSO = cma.fmin(cf.costFunctionTest2, theta, 0.5)
#resSO = cma.fmin(costFunctionTest, thetaN, 0.5, options={'popsize':5})
print(resSO[0])
t1 = time.time()
print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
#print(resSO[0])


