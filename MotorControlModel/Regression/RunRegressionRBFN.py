#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: RunRegressionRBFN

Description: We find here the function to run rbfn algorithm to create the controller
'''

import numpy as np
from shutil import copyfile

from Utils.FileSaving import saveTxt
from Utils.ReadSetupFile import ReadSetupFile
from Utils.FileReading import getStateAndCommandDataFromBrent, dicToArray

from Regression.functionApproximator_RBFN import fa_rbfn

from GlobalVariables import BrentTrajectoriesFolder

def runRBFN(name):
    ''' 
    Takes the Brent trajectories as input, shuffles them, and then runs the RBFN regression algorithm
    '''
    rs = ReadSetupFile()
    state, command = getStateAndCommandDataFromBrent(BrentTrajectoriesFolder)
    stateAll, commandAll = dicToArray(state), dicToArray(command)
    np.random.seed(0)
    np.random.shuffle(stateAll)
    np.random.seed(0)
    np.random.shuffle(commandAll)
    print("nombre d'echantillons: ", len(stateAll))
    fa = fa_rbfn(rs.numfeats,rs.inputDim,rs.outputDim)
    fa.setTrainingData(stateAll, commandAll)
    fa.setCentersAndWidths()
    fa.train_rbfn()
    savename = rs.RBFNpath + name
    saveTxt(savename, fa.theta)
    for el in rs.sizeOfTarget:
        copyfile(savename, rs.CMAESpath + str(el) + "/" + name)
    
    
    
