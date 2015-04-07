'''
Author: Thomas Beucher
Module: functionApproximator_RBFN
'''
import numpy as np
from Utils.CartesianProduct import cartesian

class fa_rbfn():
    
    def __init__(self, nbFeature):
        '''
        Initialisation des parametres de la classe
        '''
        self.nbFeat = nbFeature
        self.title = "rbfn"
        
    def setTrainingData(self, inputData, outputData):
        ##Data should be organize by columns##
        self.inputData = inputData
        self.outputData = outputData
        #Recuperation des dimensions d'entrees et de sorties ainsi que le nombre de samples
        self.inputDimension, numberOfInputSamples = np.shape(inputData)
        self.outputDimension, numberOfOutputSamples = np.shape(outputData)
        #Verification du nombre de samples pour l'entree et la sortie
        assert(numberOfInputSamples == numberOfOutputSamples), "Number of samples not equal for output and input"
        self.numberOfSamples = numberOfInputSamples
        self.theta = np.zeros((self.nbFeat, self.outputDimension))

    ################################################################################################
    #### Fonction permettant de calculer les thetas suivant l'algorithme de regression RBFN ########
    ################################################################################################
    def train_rbfn(self):
        A = np.dot(self.featureOutput(self.inputData.T), self.featureOutput(self.inputData.T).T)
        b = np.dot(self.featureOutput(self.inputData.T), self.outputData.T)
        self.theta = np.dot(np.linalg.pinv(A), b)
       

    ################################################################################################
    ## Fonction permettant de fixer les centres des gaussiennes utilisees et leurs sigma ###########
    ################################################################################################
    def setCentersAndWidths(self):
        #Recupere les minimums et maximum dans les donnees d'entrees
        minInputData = np.min(self.inputData, axis = 1)
        maxInputData = np.max(self.inputData, axis = 1)
        rangeForEachDim = maxInputData - minInputData
        #Fixe les sigmas
        widthConstant = rangeForEachDim / self.nbFeat
        print("widths: ", widthConstant, "\nMeanWidth: ", np.mean(widthConstant))
        #cree la matrice diagonales des sigmas pour le calcul de la gaussienne
        self.widths = np.diag(widthConstant)
        self.norma = 1/np.sqrt(((2*np.pi)**self.inputDimension)*np.linalg.det(self.widths)) #coef for gaussian
        linspaceForEachDim = []
        #Fixe le nombre de gaussienne utilisees et les reparties selon chaques dimensions
        for i in range(self.inputDimension):
            linspaceForEachDim.append(np.linspace(minInputData[i], maxInputData[i], self.nbFeat))
        #Permet de recuperer une matrice contenant toutes les combinaisons possibles pour trouver chaque centre
        self.centersInEachDimensions = cartesian(linspaceForEachDim)
    
    ################################################################################################
    ##### Fonction calculant les sorties, selon chaques gaussienne, pour l'entree choisie ##########
    ################################################################################################
    def featureOutput(self, inputData):
        #Si il n'y a qu'un seul echantillon
        if inputData.shape[1] == 1:
            x_u = inputData - self.centersInEachDimensions.T
            x_u_s = np.dot(x_u.T, np.linalg.pinv(self.widths))
            x = x_u_s * (x_u.T)
            xf = np.sum(x, axis = 1)
            phi = self.norma*np.exp(-0.5*xf)
        #Si il y en a plusieurs (echantillons)
        else:
            for i in range(inputData.shape[0]):
                x_u = np.array([inputData[i]]).T - self.centersInEachDimensions.T
                x_u_s = np.dot(x_u.T, np.linalg.pinv(self.widths))
                x = x_u_s * (x_u.T)
                xf = np.sum(x, axis = 1)
                xfe = self.norma*np.exp(-0.5*xf)
                if i == 0:
                    phi = np.array([xfe]).T
                else:
                    phi = np.hstack((phi, np.array([xfe]).T))
        return phi

    ################################################################################################
    ##### Fonction retournant la sortie approximee pour l'entree donnee et le theta fourni #########
    ################################################################################################
    def functionApproximatorOutput(self, inputData, theta):
        if inputData.shape[1] == 1:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        else:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        return fa_out
       
    
        