import cma
from FileProcessing.FileReading import FileReading
import time
from Regression.functionApproximator_LWR import fa_lwr
from FileProcessing.FileSaving import fileSavingStr
from Optimisation.costFunction import costFunction
import numpy as np

        
print("Debut du traitement d'optimisation!")
t0 = time.time()
fr = FileReading()
fr.getTheta(3, 0)
theta = fr.theta_store["u1"]
for i in range(5):
    theta = np.hstack((theta, fr.theta_store[str("u" + str(i+2))]))
print("la: ", theta.shape)
resSO = cma.fmin(costFunction, theta, 1)
print(resSO[0])
t1 = time.time()
print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
#print(resSO[0])


