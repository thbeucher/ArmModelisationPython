'''
Author: Thomas Beucher

Module: FileSaving

Description: On retrouve dans ce fichier les fonctions permettant de sauvegarder les donnees du projet
'''
import os as op
import pickle
from Utils.ReadSetupFile import ReadSetupFile

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
    '''
    Cette fonction permet d'enregistrer les donnees sous format str
    
    Entrees:    -nameFile: nom du fichier ou enregistrer les donnees
                -data: donnees a enregistrer
                
    '''
    rs = ReadSetupFile()
    rs.readingSetupFile()
    nameToSave = rs.pathFolderData + nameFile
    with open(nameToSave, "w") as file:
        file.write(str(data))

def fileSavingBin(nameFile, data):
    '''
    Cette fonction permet d'enregistrer les donnees sous format binaire
    
    Entrees:    -nameFile: nom du fichier ou enregistrer les donnees
                -data: donnees a enregistrer
                
    '''
    rs = ReadSetupFile()
    rs.readingSetupFile()
    nameToSave = rs.pathFolderData + nameFile
    with open(nameToSave, "wb") as file:
        monPickler = pickle.Pickler(file)
        monPickler.dump(data)
        
        
        
        