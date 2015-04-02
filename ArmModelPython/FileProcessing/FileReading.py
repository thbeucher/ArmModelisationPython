'''
Author: Thomas Beucher
Module: FileReading
'''
import pickle
import numpy as np
import math
#import cma as cma
import os.path as op
import os
from posix import getcwd
from ArmModel.ParametresRobot import ParametresRobot
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
from numpy import isnan
from ArmModel.SavingData import SavingData
from Optimisation.NiemRoot import tronquerNB
import matplotlib.pyplot as plt
#from nt import getcwd #Windows

class FileReading():
    
    def __init__(self):
        '''
        Initialisation des parametres de la classe
        '''
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
            print("Nombre de fichier disponible: ", len(os.listdir(chemin)))
            nameFichier = input("Veuillez entrer le nom courant des fichiers a traiter: ")
            nbFichier = input("Veuillez entrer le nombre de fichier à traiter: ")
            nbFichier = int(nbFichier)
        else:
            #nom du fichier courant
            nameFichier = "trajectoire"
            #nombre de fichier a traiter
            nbFichier = len(os.listdir(chemin))-1
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
    
    def recup_pos_ini(self):
        '''
        Cette fonction permet de recuperer toutes les positions initiales des trajectoires utilisees pour
        entrainer l'algorithme de regression
        '''
        print("Debut de recuperation des positions initiales!")
        chemin = getcwd()
        chemin = op.split(chemin)
        chemin = chemin[0] + "/Data/trajectoires/"
        save = SavingData()
        robot = ParametresRobot()
        angleIni = {}
        fr = FileReading()
        for el in os.listdir(chemin):
            if "trajectoire" in el:
                #Chargement du fichier
                mati = np.loadtxt(chemin + el)
                #recuperation de q1 et q2 initiales et conversion en coordonnees
                coordElbow, coordHand = save.calculCoord(np.mat([[mati[0,10]], [mati[0,11]]]), robot)
                angleIni[el] = (coordHand[0], coordHand[1])
        print("Fin de recuperation des positions initiales!")
        return angleIni
        
    ###########################################################################################
    #Cette fonction permet de récuperer q1 et q2 à partir du x et du y de la main
    ###########################################################################################
    def convertToAngle(self, xh, yh, robot):
        '''
        Cette fonction permet de récuperer q1 et q2 à partir du x et du y de la main
        '''
        q2 = math.atan2(np.sqrt(1-(xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2)), (xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2))
        #if q2 < 0:
            #q2 = q2*(-1)
        q1 = math.atan2(yh, xh)-math.atan2(robot.l2*np.sin(q2), robot.l1 + robot.l2*np.cos(q2))
        return q1, q2
    
    def mgi(self, xi, yi, robot):
        a = ((xi**2)+(yi**2)-(robot.l1**2)-(robot.l2**2))/(2*robot.l1*robot.l2)
        try:
            q2b = math.acos(a)
            cb = robot.l1 + robot.l2*(math.cos(q2b))
            db = robot.l2*(math.sin(q2b))
            q1b = math.atan2(yi,xi) - math.atan2(db,cb)
            return q1b, q2b
        except ValueError:
            print("Valeur interdite")
            return "None"
        

'''#Permet de visionner l'espace décrit par le bras humain
save = SavingData()
robot = ParametresRobot()
q1 = np.arange(-0.6,2.6,0.3)
q2 = np.arange(-0.2,3.0,0.3)
Q1,Q2 = np.meshgrid(q1,q2)
print(Q1.shape)
cor = []
for i in range(Q1.shape[0]):
    for j in range(Q1.shape[1]):
        corE, corH = save.calculCoord(np.mat([[Q1[i,j]],[Q2[i,j]]]), robot)
        cor.append(corH)
corx, cory = [], []
for el in cor:
    corx.append(el[0])
    cory.append(el[1])
plt.figure()
plt.scatter(corx,cory)
plt.show()
with open("q1q2ALL", "w+") as file:
    for i in range(Q1.shape[0]):
        for j in range(Q1.shape[1]):
            file.write(str("{"+str(Q1[i,j])+","+str(Q2[i,j])+"},"))'''


        






