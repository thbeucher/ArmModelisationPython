'''
Author: Thomas Beucher
Module: FileReading
Description: On retrouve dans ce fichier les fonctions permettant de lire les donnees du projet
'''
import pickle
import numpy as np
import os.path as op
import os
from ArmModel.ParametresRobot import ParametresRobot
from ArmModel.SavingData import SavingData
from Utils.ReadSetupFile import ReadSetupFile

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
    
    
    def getobjread(self, name):
        '''
        Fonction permettant de recuperer les donnees d'un fichier
        
        Parametres: name, le nom du fichier a lire
        
        Sorties: les donnees du fichier
        '''
        rs = ReadSetupFile()
        rs.readingSetupFile()
        namet = rs.pathFolderData + name
        with open(namet, "rb") as file:
                mondepickler = pickle.Unpickler(file)
                data = mondepickler.load()
        return data
    
    #target(4) estimated_state(4) actual_state(4) noised_command(6) command(6) estimated_next_state(4) 
    #actual_next_state(4) next_acceleration(2)
    def recup_data(self, choix = 1):
        '''
        Fonction permettant de recuperer les donnees des fichiers de trajectoires pour les ranger dans des matrices
        
        Sorties: une matrice contenant tous les etats des trajectoires et une matrice contenant toutes les activations musculaires
        '''
        rs = ReadSetupFile()
        rs.readingSetupFile()
        patht = rs.pathFolderTrajectories
        if choix == 1:
            print("Nombre de fichier disponible: ", len(os.listdir(patht)))
            nameFichier = input("Veuillez entrer le nom courant des fichiers a traiter: ")
            nbFichier = input("Veuillez entrer le nombre de fichier a traiter: ")
            nbFichier = int(nbFichier)
        else:
            #nom du fichier courant
            nameFichier = "trajectoire"
            #nombre de fichier a traiter
            nbFichier = len(os.listdir(patht))
        j = 0
        l = 0
        nbf = 0
        while j < nbFichier:
            if op.isfile(patht + nameFichier + str(j+1+nbf) + ".log") == False:
                nbf += 1
            mat = np.loadtxt(patht + nameFichier + str(j+1+nbf) + ".log")
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
        
        Sorties: un dictionnaire avec les coordonnees initiales de chaque trajectoire
        '''
        print("Debut de recuperation des positions initiales!")
        rs = ReadSetupFile()
        rs.readingSetupFile()
        patht = rs.pathFolderTrajectories
        save = SavingData()
        robot = ParametresRobot()
        angleIni = {}
        fr = FileReading()
        for el in os.listdir(patht):
            if "trajectoire" in el:
                #Chargement du fichier
                mati = np.loadtxt(patht + el)
                #recuperation de q1 et q2 initiales et conversion en coordonnees
                coordElbow, coordHand = save.calculCoord(np.mat([[mati[0,10]], [mati[0,11]]]), robot)
                angleIni[el] = (coordHand[0], coordHand[1])
        print("Fin de recuperation des positions initiales!")
        return angleIni
        
        





        






