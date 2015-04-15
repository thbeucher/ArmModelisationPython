'''
Author: Thomas Beucher

Module: costFunction

Description: On retrouve dans ce fichier 
'''
from math import sqrt
import numpy as np
import time
from Utils.FileReading import FileReading
from Utils.ThetaNormalization import vectorToMatrix
'''from ArmModel.ParametresArmModel import ParametresArmModel
from ArmModel.ParametresHogan import ParametresHogan
from ArmModel.ParametresRobot import ParametresRobot
from ArmModel.SavingData import SavingData'''
from Regression.OutputSolver import OutputSolver
from Utils.FileSaving import fileSavingStr, fileSavingBin
from Regression.functionApproximator_RBFN import fa_rbfn
import os
from Utils.ReadSetupFile import ReadSetupFile
from ArmModel.GeometricModel import mgi, mgd, jointStop
from Main.SuperToolsInit import SuperToolsInit
    
    
def costFunctionRBFN(theta):
    sti = SuperToolsInit()
    Jutmp = {}
    
    #Ce bout de code permet de generer avec le controleur toutes les trajectoires sur lesquelles il a appris
    '''data, junk = sti.fr.recup_pos_ini(sti.rs.pathFolderTrajectories)
    for key, el in data.items():
        Ju = sti.trajGenerator(el[0], el[1], theta)
        JuCf.append((key, Ju))'''
    '''posi = []
    for i in range(10):
        posi.append(sti.posIni[0])'''
    #Le nombre d'iteration pour i donne le nombre de trajectoire realises
    for i in range(5):
        JuCf = []
        for el in sti.posIni:
            Ju = sti.trajGenerator(el[0], el[1], theta)
            JuCf.append(Ju)
        Jutmp[i] = JuCf
    s = 0
    for el in Jutmp.values():
        if s == 0:
            juju = np.array(el)
            s += 1
        else:
            juju = np.vstack((juju, el))
    meanJu = np.mean(juju, axis = 0)
    return JuCf, sti

class costFunctionClass:
    
    def __init__(self):
        self.call = 0
              
    def costFunctionCMAES(self, theta):
        sti = SuperToolsInit()
        Jutmp = {}
        maxT = sti.fr.getobjread("OptimisationResults/maxTBIN")
        theta = theta*maxT
        theta = vectorToMatrix(theta)
        
        for i in range(5):
            JuCf = []
            for el in sti.posIni:
                Ju = sti.trajGenerator(el[0], el[1], theta)
                JuCf.append(Ju*-1)
            Jutmp[i] = JuCf
        s = 0
        for el in Jutmp.values():
            if s == 0:
                juju = np.array(el)
                s += 1
            else:
                juju = np.vstack((juju, el))
        meanJu = np.mean(juju, axis = 0)
        JuSca = np.mean(meanJu)
        print(self.call)
        self.call += 1
        return JuSca



