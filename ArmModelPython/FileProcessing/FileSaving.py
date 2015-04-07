#######################################################################################
########## Author: Thomas Beucher // Module: FileSaving ###############################
#######################################################################################
import os as op
import pickle
from posix import getcwd
from Script.ReadSetupFile import ReadSetupFile
#from nt import getcwd #Windows for posix

def fileSaving(nameFile, data, nbfeat):
    rs = ReadSetupFile()
    rs.readingSetupFile()
    folder = rs.pathFolderData + "RegressionResults/"
    folderNbFeat = folder + str(nbfeat) + "_feats"
    if not op.path.exists(folderNbFeat): 
        op.makedirs(folderNbFeat)
    folder = folderNbFeat + "/"
    nameToSave = folder + nameFile
    with open(nameToSave, "wb") as file:
        monPickler = pickle.Pickler(file)
        monPickler.dump(data)
        
def fileSavingStr(nameFile, data):
    rs = ReadSetupFile()
    rs.readingSetupFile()
    nameToSave = rs.pathFolderData + nameFile
    with open(nameToSave, "w") as file:
        file.write(str(data))

def fileSavingBin(nameFile, data):
    rs = ReadSetupFile()
    rs.readingSetupFile()
    nameToSave = rs.pathFolderData + nameFile
    with open(nameToSave, "wb") as file:
        monPickler = pickle.Pickler(file)
        monPickler.dump(data)
        
        
        
        