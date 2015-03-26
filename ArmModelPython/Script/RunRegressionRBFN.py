from FileProcessing.FileReading import FileReading
from FileProcessing.FileSaving import fileSavingBin, fileSavingStr
from Regression.functionApproximator_RBFN import fa_rbfn
import time



def runRBFN(nbfeat):
    t0 = time.time()
    print("Début de traitement!")
    fr = FileReading()
    stateAll, commandAll = fr.recup_data(0)
    
    fa = fa_rbfn(nbfeat)
    fa.setTrainingData(stateAll.T, commandAll.T)
    fa.setCentersAndWidths()
    fa.train_rbfn()
    nameSaveStr = "RBFN2/" + str(nbfeat) + "feats/Theta"
    nameSaveBin = "RBFN2/" + str(nbfeat) + "feats/ThetaBIN"
    fileSavingStr(nameSaveStr, fa.theta)
    fileSavingBin(nameSaveBin, fa.theta)
    t1 = time.time()
    print("Fin du traitement! (temps d'execution:", (t1-t0), "s)")