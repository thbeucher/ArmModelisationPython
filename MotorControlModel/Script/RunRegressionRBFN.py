#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: RunRegressionRBFN

Description: We find here the function to run rbfn algorithm to create the controller
'''
import time
import numpy as np
from Utils.InitUtil import initFRRS
from Regression.functionApproximator_RBFN import fa_rbfn
from Utils.FileSaving import fileSavingStrJson


####################################################################################################
## runRBFN permet de lancer l'algorithme de regression sur les données de trajectoires du brent ####
####################################################################################################
def runRBFN(nameSaveC):
    print("Début de traitement!")
    t0 = time.time()
    fr, rs = initFRRS()
    state, command = fr.getData(rs.pathFolderTrajectories)
    #change the data (dictionary) into numpy array
    stateAll, commandAll = fr.dicToArray(state), fr.dicToArray(command)
    np.random.seed(0)
    np.random.shuffle(stateAll)
    np.random.seed(0)
    np.random.shuffle(commandAll)
    print("nombre d'echantillons: ", stateAll.shape[0])
    fa = fa_rbfn(rs.numfeats)
    fa.setTrainingData(stateAll.T, commandAll.T)
    fa.setCentersAndWidths()
    fa.train_rbfn()
    name = "RBFN2/" + str(rs.numfeats) + "feats/" + nameSaveC
    fileSavingStrJson(name, fa.theta)
    t1 = time.time()
    print("Fin du traitement! (temps d'execution:", (t1-t0), "s)")
    
    
    