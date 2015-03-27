#######################################################################################
########## Author: Thomas Beucher // Module: FileReading ##############################
#######################################################################################
import pickle
import numpy as np
import math as ma
#import cma as cma
import os.path as op
from posix import getcwd
from ArmModel.ParametresRobot import ParametresRobot
from FileProcessing.FileSaving import fileSavingStr
#from nt import getcwd #Windows

class FileReading():
    
    def __init__(self):
        #Recuperation des commandes
        self.uCommand = {}
        self.data_store = {}   
        self.name_store = []
        self.theta_store = {}
    
    ################################################################################################
    ######################## Fonction permettant de récupérer les données d'un fichier #############
    ################################################################################################
    def getobjread(self, name):
        folder = getcwd()
        folder = op.split(folder)
        folder = folder[0] + "/Data/"
        namet = folder + name
        with open(namet, "rb") as file:
                mondepickler = pickle.Unpickler(file)
                data = mondepickler.load()
        return data
    
    #target(4) estimated_state(4) actual_state(4) noised_command(6) command(6) estimated_next_state(4) 
    #actual_next_state(4) next_acceleration(2)
    #Recuperation des donnees du fichier dans une matrice
    def recup_data(self, choix = 1):
        chemin = getcwd()
        chemin = op.split(chemin)
        chemin = chemin[0] + "/Data/trajectoires/"
        if choix == 1:
            nameFichier = input("Veuillez entrer le nom courant des fichiers a traiter: ")
            nbFichier = input("Veuillez entrer le nombre de fichier à traiter: ")
            nbFichier = int(nbFichier)
        else:
            #nom du fichier courant
            nameFichier = "trajectoire"
            #nombre de fichier a traiter
            nbFichier = 12
        j = 0
        l = 0
        nbf = 0
        while j < nbFichier:
            if op.isfile(chemin + nameFichier + str(j+1+nbf) + ".log") == False:
                nbf += 1
            mat = np.loadtxt(chemin + nameFichier + str(j+1+nbf) + ".log")
            i = 0
            k = 0
            state = []
            command = []
            while i < mat.size/34:
                state.append((mat[i][k+8], mat[i][k+9], mat[i][k+10], mat[i][k+11]))
                command.append((mat[i][k+18], mat[i][k+19], mat[i][k+20], mat[i][k+21], mat[i][k+22], mat[i][k+23]))
                i += 1
            self.data_store[str(nameFichier + str(j+1+nbf) + "_state")] = state
            self.data_store[str(nameFichier + str(j+1+nbf) + "_command")] = command
            self.name_store.append(str(nameFichier + str(j+1+nbf)))
            if l == 0:
                stateAll = np.array(state)
                commandAll = np.array(command)
                l += 1
            else:
                stateAll = np.vstack((stateAll, state))
                commandAll = np.vstack((commandAll, command))
            j += 1
        return stateAll, commandAll
    
    
    ###########################################################################################
    #Cette fonction permet de récupérer q1 et q2 à partir du x et du y de la main
    ###########################################################################################
    def convertToAngle(self, xh, yh, robot):
        q2 = ma.atan2(np.sqrt(1-(xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2)), (xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2))
        if q2 < 0:
            q2 = q2*(-1)
        q1 = ma.atan2(yh, xh)-ma.atan2(robot.l2*np.sin(q2), robot.l1 + robot.l2*np.cos(q2))
        return q1, q2


#Bout de code pour generer les q1, q2 associes aux positions initiales
'''a = []
a.append((-0.2,0.39))
a.append((-0.1,0.39))
a.append((0.0,0.39))
a.append((0.1,0.39))
a.append((0.2,0.39))
a.append((-0.3,0.26))
a.append((-0.2,0.26))
a.append((-0.1,0.26))
a.append((0.0,0.26))
a.append((0.1,0.26))
a.append((0.2,0.26))
a.append((0.3,0.26))

q = []
fr = FileReading()
robot = ParametresRobot()
for el in a:
    q.append(fr.convertToAngleTest(el[0], el[1], robot))
fileSavingStr("q1q2ForPosIni", q)
print(q)'''


