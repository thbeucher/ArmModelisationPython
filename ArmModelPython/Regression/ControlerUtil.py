#######################################################################################
########## Author: Thomas Beucher // Module: ControlerUtil ############################
#######################################################################################
from FileProcessing.FileReading import FileReading
import numpy as np

class ControlerUtil:
    def __init__(self, nbfeature, dime):
        self.nbfeat = nbfeature
        self.dim = dime

    ########################################################################
    # Fonction permettant de recuperer la sortie des activations musculaires
    ########################################################################
    def getCommand(self, inputgc, numTrajectoire, fa, theta):
        self.U = fa.functionApproximatorOutput(inputgc, theta)

        
        