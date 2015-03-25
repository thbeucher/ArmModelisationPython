from FileProcessing.FileReading import FileReading
import numpy as np

class ControlerUtil:
    def __init__(self, nbfeature, dime):
        self.nbfeat = nbfeature
        self.dim = dime

    def getCommand(self, inputgc, numTrajectoire, fa, theta):
        self.U = fa.functionApproximatorOutput(inputgc, theta)

        
        