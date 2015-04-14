'''
Author: Thomas Beucher
Module: FileReading
Description: On retrouve dans ce fichier les fonctions permettant de lire les donnees du projet
'''
import pickle
import numpy as np
import os.path as op
import os
from Utils.ReadSetupFile import ReadSetupFile
from ArmModel.GeometricModel import mgd, mgi
from ArmModel.ArmParameters import ArmParameters
from Utils.NiemRoot import tronquerNB
from shutil import copyfile
import matplotlib.pyplot as plt

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
    
    
    
    def recup_pos_ini(self, location):
        '''
        Cette fonction permet de recuperer toutes les positions initiales des trajectoires utilisees pour
        entrainer l'algorithme de regression
        
        Sorties: un dictionnaire avec les coordonnees initiales de chaque trajectoire
        '''
        print("Debut de recuperation des positions initiales!")
        armP = ArmParameters()
        angleIni = {}
        Q = []
        for el in os.listdir(location):
            if "trajectoire" in el:
                #Chargement du fichier
                mati = np.loadtxt(location + el)
                Q.append((el, mati[0,10], mati[0,11]))
                #recuperation de q1 et q2 initiales et conversion en coordonnees
                coordElbow, coordHand = mgd(np.mat([[mati[0,10]], [mati[0,11]]]), armP.l1, armP.l2)
                angleIni[el] = (coordHand[0], coordHand[1])
        print("Fin de recuperation des positions initiales!")
        return angleIni, Q
 
 
    def getData(self, location):
        '''
        This function get all the states and commands of trajectories available
        
        Outputs:    -state: dictionary
                    -command: dictionary
        '''
        state, command = {}, {}
        for el in os.listdir(location):
            state[el], command[el] = [], []
        for el in os.listdir(location):
            mati = np.loadtxt(location + el)
            for i in range(mati.shape[0]):
                state[el].append((mati[i][8], mati[i][9], mati[i][10], mati[i][11]))
                command[el].append((mati[i][18], mati[i][19], mati[i][20], mati[i][21], mati[i][22], mati[i][23]))
        return state, command
    
    def dicToArray(self, data):
        '''
        This function transform a dictionary in an array
        
        Input:     -data: dictionary
        
        Output:    -dataA: numpy array
        '''
        i = 0
        for el in data.values():
            if i == 0:
                dataA = np.array(el)
            else:
                dataA = np.vstack((dataA, np.array(el)))
            i += 1
        return dataA
            
            

            
            

        






