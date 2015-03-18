import os as op
import pickle
from posix import getcwd

def fileSaving(nameFile, data, nbfeat):
    folder = getcwd()
    folder = op.path.split(folder)
    folder = folder[0] + "/FileProcessing/RegressionResults/"
    folderNbFeat = folder + str(nbfeat) + "_feats"
    if not op.path.exists(folderNbFeat): 
        op.makedirs(folderNbFeat)
    folder = folderNbFeat + "/"
    nameToSave = folder + nameFile
    with open(nameToSave, "wb") as file:
        monPickler = pickle.Pickler(file)
        monPickler.dump(data)
        
def fileSavingStr(nameFile, data):
    folder = getcwd()
    folder = op.path.split(folder)
    folder = folder[0] + "/FileProcessing/ControlerResult/"
    nameToSave = folder + nameFile
    with open(nameToSave, "w") as file:
        file.write(str(data))
        