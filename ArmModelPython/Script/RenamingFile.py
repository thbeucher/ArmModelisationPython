import os
from posix import getcwd

def renameFromOutputSOlver():
    print("Debut de traitement!")
    i = 13
    patho = "/home/beucher/Desktop/Monfray/Codes/Java/output_solver/"
    for el in os.listdir(patho):
        if el.endswith('.log'):
            if "failed" in el:
                pass
            else:
                os.rename(patho + el, str(patho + "trajectoire" + str(i)))
                i += 1
    print("Fin de traitement!")
    
def renameFromTrajectoires():
    patho = "/home/beucher/workspace/ArmModelPython/Data/trajectoires/"
    for el in os.listdir(patho):
        if not ".log" in el:
            os.rename(patho + el, str(patho + el + ".log"))
        
