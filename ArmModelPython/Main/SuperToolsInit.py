'''
Author: Thomas Beucher

Module: SuperToolsInit

Description: On retrouve dans ce fichier une classe initialisant toutes les classes utiles au projet
'''
from ArmModel.ParametresArmModel import ParametresArmModel
from ArmModel.ParametresHogan import ParametresHogan
from ArmModel.ParametresRobot import ParametresRobot
from ArmModel.SavingData import SavingData
from Utils.FileReading import FileReading
from Utils.ReadSetupFile import ReadSetupFile
from Regression.functionApproximator_RBFN import fa_rbfn
import numpy as np



class SuperToolsInit:
    
    def __init__(self):
        '''
        Initialisation des parametres de classe
        '''
        self.super = "SuperInit"
        self.robot = ParametresRobot()
        self.hogan = ParametresHogan()
        self.arm = ParametresArmModel(self.hogan.GammaMax)
        self.save = SavingData()
        self.fr = FileReading()
        self.rs = ReadSetupFile()
        self.rs.readingSetupFile()
        #Initialisation des outils permettant d'utiliser le controleur rbfn
        self.fa = fa_rbfn(self.rs.numfeats)
        stateAll, commandAll = self.fr.recup_data(0)
        self.fa.setTrainingData(stateAll.T, commandAll.T)
        self.fa.setCentersAndWidths()
        #Recuperation des positions initiales de l'experimentation
        self.posIni = self.fr.getobjread("PosIniExperiment1")
    
    def initParamTraj(self):
        pass
    
    def costFunction(self, Ju, U, t):
        '''
        Cette fonction permet de calculer le cout d'une trajectoire en terme d'activation musculaire
            
        Entrees:    -Ju: scalar, cout de la trajectoire a l'instant t
                    -U: 1D numpy array, Activations musculaires
                    -t: scalar
        '''
        mvtCost = (np.linalg.norm(U))**2
        Ju += np.exp(-t/self.rs.gammaCF)*(self.rs.upsCF*mvtCost)
        return Ju
        
        
    def getCommand(self, inputgc, theta):
        '''
        Fonction permettant de recuperer la sortie des activations musculaires
            
        Entrees:    -inputgc: tableau des entrees dont on cherche la sortie approximee
                    -theta: 2D numpy array, tableau donnant les poids des gaussiennes servant a approximer la fonction utilisee
        
        Sortie:    -Unoise: 1D numpy array, vecteur des activations musculaires bruitees
        '''
        U = self.fa.functionApproximatorOutput(inputgc, theta)
        #Pas d'activations musculaires négatives possibles
        for i in range(U.shape[0]):
            if U[i] < 0:
                U[i] = 0
            elif U[i] > 1:
                U[i] = 1
        #Bruit d'activation musculaire 
        UnoiseTmp = U*(1+np.random.normal(0,self.rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = UnoiseTmp
        return Unoise
        
        
        
        
