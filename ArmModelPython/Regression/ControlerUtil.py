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
        #Bruit d'activation musculaire / nombre aléatoire entre 0 et 1
        noise = np.random.rand(6)
        self.Unoise = np.array(self.U*noise)
        
        