import os
from posix import getcwd
from shutil import copyfile

def renameFromOutputSOlver():
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
                os.rename(patho + el, str(patho + "trajectoire" + str(i)))
                copyfile(str(patho + "trajectoire" + str(i)), str(pathin + "trajectoire" + str(i)))
                i += 1
    print("Fin de traitement!")
    
def renameFromTrajectoires():
    patho = "/home/beucher/workspace/ArmModelPython/Data/trajectoires/"
    for el in os.listdir(patho):
        if not ".log" in el:
            os.rename(patho + el, str(patho + el + ".log"))
        
renameFromOutputSOlver()
renameFromTrajectoires()