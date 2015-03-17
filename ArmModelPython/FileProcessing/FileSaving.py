import os as op
from nt import getcwd

def fileSaving(nameFile, data, nbfeat):
    folder = getcwd()
    folder = op.path.split(folder)
    folder = folder[0] + "/FileProcessing/RegressionResults/"
    folderNbFeat = folder + str(nbfeat) + "feats"
    if not op.path.exists(folderNbFeat): 
        op.makedirs(folderNbFeat)
    folder = folderNbFeat + "/"
    nameToSave = folder + nameFile
    with open(nameToSave, "w") as file:
        file.write(str(data))
        