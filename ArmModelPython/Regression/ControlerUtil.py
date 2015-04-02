'''
Author: Thomas Beucher
Module: ControlerUtil
'''
from FileProcessing.FileReading import FileReading
import numpy as np
import bigfloat
from Script.ReadSetupFile import ReadSetupFile

class ControlerUtil:
    def __init__(self, nbfeature, dime):
        '''
        Initialisation des parametres de la classe
        '''
        self.nbfeat = nbfeature
        self.dim = dime

    ########################################################################
    # Fonction permettant de recuperer la sortie des activations musculaires
    ########################################################################
    def getCommand(self, inputgc, numTrajectoire, fa, theta):
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

        
        