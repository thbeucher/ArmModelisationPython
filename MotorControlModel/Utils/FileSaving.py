#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: FileSaving

Description: Functions to save data into files
'''
import os
import json
import pickle
import numpy as np

def checkIfFolderExists(name):
    if not os.path.isdir(name):
        os.makedirs(name)

def saveTxt(fileName, data):
    '''
    Records data under str format
    
    Input:    -fileName: name of the file where data will be recorded
                -data: recorded data
                
    '''
    print ("txt taille", len(data))
    np.savetxt(fileName, data)
       
        
