'''
Author: Thomas Beucher
Module: ControlerUtil
'''
from FileProcessing.FileReading import FileReading
import numpy as np
import bigfloat

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
        self.U = fa.functionApproximatorOutput(inputgc, theta)
        #Bruit d'activation musculaire / nombre aléatoire entre 0 et 1
        self.Unoise = np.divide(np.log(np.exp(500*self.U) + 1), 500)

        
        