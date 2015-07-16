#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: DataNormalization

Description: We find here functions which normalize the input data
'''

import numpy as np
from Utils.FileSaving import fileSavingBin

def normData(inputData):
    maxABSInputData = np.max(np.abs(inputData))
    fileSavingBin("RegressionInfo/maxABSInputData", maxABSInputData)
    inputData = inputData/maxABSInputData
    return inputData

def normDataForEachIndividualColumns(inputData):
    maxABSInputData = np.max(np.abs(inputData), axis = 1)
    for i in range(inputData.shape[0]):
        inputData[i,:] = inputData[i,:] / maxABSInputData[i]
    return inputData