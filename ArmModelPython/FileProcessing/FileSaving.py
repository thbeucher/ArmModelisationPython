import os.path as op
from nt import getcwd

def fileSaving(nameFile, data):
    folder = getcwd()
    folder = op.split(folder)
    folder = folder[0] + "/FileProcessing/RegressionResults/"
    nameToSave = folder + nameFile
    with open(nameToSave, "w") as file:
        file.write(str(data))
        