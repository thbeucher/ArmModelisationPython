#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: RunRegressionRBFN

Description: We find here the function to run rbfn algorithm to create the controller
'''

import os
import numpy as np
import random as rd
from shutil import copyfile

from Utils.ReadSetupFile import ReadSetupFile
from Utils.FileReading import getStateAndCommandData, dicToArray

from Regression.RBFN import rbfn
from Experiments.TrajMaker import initRBFNController

from GlobalVariables import BrentTrajectoriesFolder

def runRBFN(name):
    ''' 
    Takes the Brent trajectories as input, shuffles them, and then runs the RBFN regression algorithm
    '''
    rs = ReadSetupFile()
    state, command = getStateAndCommandData(BrentTrajectoriesFolder)
    stateAll, commandAll = dicToArray(state), dicToArray(command)
    np.random.seed(0)
    np.random.shuffle(stateAll)
    np.random.seed(0)
    np.random.shuffle(commandAll)
    print("nombre d'echantillons: ", len(stateAll))
    fa = rbfn(rs.numfeats,rs.inputDim,rs.outputDim)
    fa.setTrainingData(stateAll, commandAll)
    fa.train_rbfn()
    saveThetaControllers(rs,name,fa)
    #test(fa, stateAll)

def saveThetaControllers(rs, name, fa):
    savename = rs.RBFNpath + name
    fa.saveTheta(savename)
    for el in rs.sizeOfTarget:
        copyfile(savename, rs.CMAESpath + str(el) + "/" + name)
    
def test(fa, state):
    for el in state:
        if rd.random()<0.06:
            retour = fa.computeOutput(el)
            print("in:", el)
            print(" out:", retour)

def UnitTest():
    fa = rbfn(3,2,3)
    input, output = [], []
    for i in range(10000):
        x,y = rd.random(), rd.random()
        input.append([x,y])
        output.append([x*y, x-y, x+y])
    fa.setTrainingData(np.vstack(np.array(input)), np.vstack(np.array(output)))
    fa.train_rbfn()
    fa.saveTheta("test")

    fa.loadTheta("test")
    for i in range(20):
        x,y = 3*rd.random(), 3*rd.random()
        approx = fa.computeOutput(np.array([x,y]))
        print("in:", [x,y])
        print(" out:", approx)
        print(" real:",  [x*y, x-y, x+y])
  
def UnitTestRBFNController():
    '''
    Tests the approximated command obtained from training states
    '''
    rs = ReadSetupFile()
    fa = initRBFNController(rs)
    fa.train_rbfn()
    fa.saveTheta("test")

    fa.loadTheta("test")

    state, command = {}, {}
    for el in os.listdir(BrentTrajectoriesFolder):
            state[el], command[el] = [], []
            data = np.loadtxt(foldername + el)
            for i in range(data.shape[0]):
                state[el].append((data[i][8], data[i][9], data[i][10], data[i][11]))
                command[el].append((data[i][18], data[i][19], data[i][20], data[i][21], data[i][22], data[i][23]))

    for el in os.listdir(foldername):
            for i in range(len(state[el])):
                outrbfn = fa.computeOutput(np.array(state[el][i]))
                print("Real  :", command[el][i]) 
                print("Learn :",outrbfn)

    
    
