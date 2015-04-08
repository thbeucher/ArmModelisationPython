'''
Author: Thomas Beucher

Module: RenamingFile

Description: On retrouve dans ce fichier les fonctions permettant de recuperer les trajectoires generees par brent et de les importer
                sous le nom "trajectoire" dans le dossier trajectoires
'''
import os
from shutil import copyfile
from Utils.ReadSetupFile import ReadSetupFile

def renameFromOutputSOlver():
    '''
    Cette fonction permet de recuperer les trajectoires disponibles dans le dossier outputSolver, de les renommer
    et de les importer dans l'espace de travail du projet
    '''
    print("Debut de traitement!")
    rs = ReadSetupFile()
    rs.readingSetupFile()
    i = len(os.listdir(rs.pathFolderTrajectories))
    print(i)
    patho = "/home/beucher/Desktop/Monfray/Codes/Java/output_solver/"
    for el in os.listdir(patho):
        if el.endswith('.log'):
            if "failed" in el:
                pass
            else:
                os.rename(patho + el, str(patho + "trajectoire" + str(i+1)))
                copyfile(str(patho + "trajectoire" + str(i+1)), str(rs.pathFolderTrajectories + "trajectoire" + str(i+1)))
                i += 1
    print("Fin de traitement!")
    
def renameFromTrajectoires():
    rs = ReadSetupFile()
    rs.readingSetupFile()
    for el in os.listdir(rs.pathFolderTrajectories):
        if not ".log" in el:
            os.rename(rs.pathFolderTrajectories + el, str(rs.pathFolderTrajectories + el + ".log"))
        
renameFromOutputSOlver()
renameFromTrajectoires()