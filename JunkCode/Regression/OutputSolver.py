'''
Author: Thomas Beucher

Module: OutputSolver

Description: On retrouve dans ce fichier la fonction permettant de donner la sortie approxime en fonction de l'entree fournie
'''
from Utils.FileReading import FileReading
import numpy as np
import bigfloat
from Utils.ReadSetupFile import ReadSetupFile

class OutputSolver:
    def __init__(self, nbfeature, dime):
        '''
        Initialisation des parametres de la classe
        '''
        self.nbfeat = nbfeature
        self.dim = dime

    def getCommand(self, inputgc, fa, theta):
        '''
        Fonction permettant de recuperer la sortie des activations musculaires
        
        Entrees:    -inputgc: tableau des entrees dont on cherche la sortie approximee
                    -fa: objet permettant l'acces a la fonction de recuperation de la sortie approximee
                    -theta: tableau donnant les poids des gaussiennes servant a approximer la fonction utilisee
        '''
        U = fa.functionApproximatorOutput(inputgc, theta)
        #Recuperation de la valeur de k pour le bruit moteur
        rs = ReadSetupFile()
        rs.readingSetupFile()
        #Pas d'activations musculaires négatives possibles
        for i in range(U.shape[0]):
            if U[i] < 0:
                U[i] = 0
            elif U[i] > 1:
                U[i] = 1
        self.U = U
        #Bruit d'activation musculaire
        
        UnoiseTmp = U*(1+np.random.normal(0,rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        self.Unoise = UnoiseTmp



        
        