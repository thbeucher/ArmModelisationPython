#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher
Module: PurgeData
Description: the function below alow to purge temporary data
'''
from Utils.InitUtil import initFRRS
from GlobalVariables import pathDataFolder
import numpy as np


def purgeCostNThetaTmp(sizeOfTarget):
    '''
    
    '''
    nameFileSave = pathDataFolder + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/thetaSolTmp_target" + str(sizeOfTarget)
    nameFileSaveMeanCost = pathDataFolder + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/meanCost" + str(sizeOfTarget)
    a = np.loadtxt(nameFileSave)
    b = np.loadtxt(nameFileSaveMeanCost)
    nameFileSave1 = nameFileSave + "OldTmp"
    nameFileSaveMeanCost1 = nameFileSaveMeanCost + "OldTmp"
    f = open(nameFileSave1, "wb")
    g = open(nameFileSaveMeanCost1, "wb")
    np.savetxt(f, a)
    np.savetxt(g, b)
    #purge file
    f = open(nameFileSave, "w")
    g = open(nameFileSaveMeanCost, "w")
        
        
        

