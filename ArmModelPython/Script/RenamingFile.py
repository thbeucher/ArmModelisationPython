'''
Author: Thomas Beucher
Module: RenamingFile
'''
import os
from posix import getcwd
from shutil import copyfile

def renameFromOutputSOlver():
    '''
    Cette fonction permet de recuperer les trajectoires disponibles dans le dossier outputSolver, de les renommer
    et de les importer dans l'espace de travail du projet
    '''
    print("Debut de traitement!")
    pathin = "/home/beucher/workspace/ArmModelPython/Data/trajectoires/"
    i = len(os.listdir(pathin))
    print(i)
    patho = "/home/beucher/Desktop/Monfray/Codes/Java/output_solver/"
    for el in os.listdir(patho):
        if el.endswith('.log'):
            if "failed" in el:
                pass
            else:
                os.rename(patho + el, str(patho + "trajectoire" + str(i+1)))
                copyfile(str(patho + "trajectoire" + str(i+1)), str(pathin + "trajectoire" + str(i+1)))
                i += 1
    print("Fin de traitement!")
    
def renameFromTrajectoires():
    patho = "/home/beucher/workspace/ArmModelPython/Data/trajectoires/"
    for el in os.listdir(patho):
        if not ".log" in el:
            os.rename(patho + el, str(patho + el + ".log"))
        
renameFromOutputSOlver()
renameFromTrajectoires()