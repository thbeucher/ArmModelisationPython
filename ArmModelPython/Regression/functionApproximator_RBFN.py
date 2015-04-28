'''
Author: Thomas Beucher

Module: functionApproximator_RBFN

Description: We find here functions which allow to compute a RBFN regression
'''
import numpy as np
from Utils.CartesianProduct import cartesian
from multiprocessing.context import Process
from multiprocessing.sharedctypes import Array
import ctypes as ct
from Utils.DataNormalization import normData, normDataForEachIndividualColumns


class fa_rbfn():
    
    def __init__(self, nbFeature):
        '''
        Initialization of class parameters
        
        Input:     -nbFeature: int, number of feature in order to perform the regression
        
        '''
        self.nbFeat = nbFeature
        self.title = "rbfn"
        
    def setTrainingData(self, inputData, outputData):
        '''
        This function verify the validity of input and output data given
        Data should be organize by columns
        
        Input:      -inputdata, numpy N-D array
                    -outputData, numpy N-D array
        '''
        #inputData = normData(inputData)
        #inputData = normDataForEachIndividualColumns(inputData)
        #outputData = normDataForEachIndividualColumns(outputData)
        
        self.inputData = inputData
        self.outputData = outputData
        #Recuperation des dimensions d'entrees et de sorties ainsi que le nombre de samples
        self.inputDimension, numberOfInputSamples = np.shape(inputData)
        self.outputDimension, numberOfOutputSamples = np.shape(outputData)
        #Verification du nombre de samples pour l'entree et la sortie
        assert(numberOfInputSamples == numberOfOutputSamples), "Number of samples not equal for output and input"
        self.numberOfSamples = numberOfInputSamples
        self.theta = np.zeros((self.nbFeat, self.outputDimension))

    def computeA(self, A, fop):
        A = np.dot(fop, fop.T)
        print("ici2", A[0])
        
    def computeb(self, b, fop):
        b = np.dot(fop, self.outputData.T)
        print("iciaussi", b[0])
    
    def train_rbfn(self):
        '''
        The training function to find solution of the approximation
        
        '''
        #A = np.dot(self.featureOutput(self.inputData.T), self.featureOutput(self.inputData.T).T)
        #b = np.dot(self.featureOutput(self.inputData.T), self.outputData.T)
        fop = self.featureOutput(self.inputData.T)
        '''n = self.nbFeat**self.inputDimension
        AshareObj = Array(ct.c_double, n*n)
        bshareObj = Array(ct.c_double, n*self.outputDimension)
        AnumpyShare = np.frombuffer(AshareObj.get_obj())
        bnumpyShare = np.frombuffer(bshareObj.get_obj())
        A = AnumpyShare.reshape((n, n))
        b = bnumpyShare.reshape((n, self.outputDimension))
        p1 = Process(target=self.computeA, args=(A, fop))
        p2 = Process(target=self.computeb, args=(b, fop))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        print("la", A[0], "\n", b[0])
        c = input("la2")'''
        A = np.dot(fop, fop.T)
        b = np.dot(fop, self.outputData.T)
        self.theta = np.dot(np.linalg.pinv(A), b)
       
    def setCentersAndWidths(self):
        '''
        Function which set the centers and widths of Gaussian used
        
        '''
        #Recupere les minimums et maximum dans les donnees d'entrees
        minInputData = np.min(self.inputData, axis = 1)
        maxInputData = np.max(self.inputData, axis = 1)
        rangeForEachDim = maxInputData - minInputData
        #Fixe les sigmas
        widthConstant = rangeForEachDim / self.nbFeat
        #print("widths: ", widthConstant, "\nMeanWidth: ", np.mean(widthConstant))
        #cree la matrice diagonales des sigmas pour le calcul de la gaussienne
        self.widths = np.diag(widthConstant)
        self.norma = 1/np.sqrt(((2*np.pi)**self.inputDimension)*np.linalg.det(self.widths)) #coef for gaussian
        linspaceForEachDim = []
        #Fixe le nombre de gaussienne utilisees et les reparties selon chaques dimensions
        for i in range(self.inputDimension):
            linspaceForEachDim.append(np.linspace(minInputData[i], maxInputData[i], self.nbFeat))
        #Permet de recuperer une matrice contenant toutes les combinaisons possibles pour trouver chaque centre
        self.centersInEachDimensions = cartesian(linspaceForEachDim)
    
    def featureOutput(self, inputData):
        '''
        Computation of gaussian
        
        Input:     -inputData: numpy N-D array
        
        Output:    -phi: numpy N-D array
        '''
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


    def functionApproximatorOutput(self, inputData, theta):
        '''
        Function which return the output depend of the input and theta given
        
        Input:      -inputData: numpy N-D array
                    -theta: numpy N-D array
        
        Output:     -fa_out: numpy N-D array, output approximated
        '''
        if inputData.shape[1] == 1:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        else:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        return fa_out
       
    
        