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
        
#Lecture des fichiers de trajectoire
fileR = FileReading()
stateAll, commandAll = fileR.recup_data(2)
fa = fa_lwr(3, 4, fileR.data_store, fileR.name_store, 3)
print("Debut du traitement d'optimisation!")
t0 = time.time()
fileR.tabActivationMuscu("AllCommand", commandAll, True)
cs = Cmaes()
for i in range(6):
    name = str("AllCommand_u" + str(i+1))
    resSO = cs.stochastiqueOptimisation(fa.train_LS(stateAll, fileR.uCommand[name]), fileR.uCommand[name], fa.widthConstant)
    nameToSave = "OptimisationResults/ThetaOpti_u" + str(i+1)
    fileSavingStr(nameToSave, resSO)
t1 = time.time()
print("Fin de l'optimisation! (Temps de traitement: ", (t1-t0), "s)")
print(resSO)


