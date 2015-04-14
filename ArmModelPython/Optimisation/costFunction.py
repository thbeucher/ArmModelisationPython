'''
Author: Thomas Beucher

Module: costFunction

Description: On retrouve dans ce fichier 
'''
from math import sqrt
import numpy as np
import time
from Utils.FileReading import FileReading
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
    JuCf = []
    
    '''data, junk = sti.fr.recup_pos_ini(sti.rs.pathFolderTrajectories)
    for key, el in data.items():
        Ju = sti.trajGenerator(el[0], el[1], theta)
        JuCf.append((key, Ju))'''
    
    for el in sti.posIni:
        Ju = sti.trajGenerator(el[0], el[1], theta)
        JuCf.append(Ju)
    return JuCf, sti

        



    

