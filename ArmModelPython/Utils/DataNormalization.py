'''
Author: Thomas Beucher

Module: DataNormalization

Description: We find here functions which normalize the input data
'''
import numpy as np
from Utils.FileSaving import fileSavingBin

def normData(inputData):
    maxABSInputData = np.max(np.abs(inputData), axis = 1)
    fileSavingBin("RegressionInfo/maxABSInputData", maxABSInputData)
    inputData = inputData/maxABSInputData
    return inputData