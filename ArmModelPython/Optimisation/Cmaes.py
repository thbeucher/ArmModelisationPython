import cma
from FileProcessing.FileReading import FileReading
import time
from Regression.functionApproximator_LWR import fa_lwr
from FileProcessing.FileSaving import fileSavingStr

class Cmaes:
    
    def __init__(self):
        self.ok = "ok"
        
    def stochastiqueOptimisation(self, objective_function, x0, sigma0):
        res = cma.fmin(objective_function, x0, sigma0)
        return res
        

print("Debut du traitement d'optimisation!")
t0 = time.time()

t1 = time.time()
print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
#print(resSO[0])


