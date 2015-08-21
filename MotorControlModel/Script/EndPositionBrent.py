'''
Author: Thomas Beucher

Module: EndPositionbrent 

Description: We find here a script which print the end positions of brent trajectories
'''
import sys
name = "/home/beucher/ProjetCluster/ArmModelPython/"
sys.path.append(name + "Utils")
sys.path.append(name + "ArmModel")
sys.path.append(name + "Main")
sys.path.append(name + "Regression")
sys.path.append(name + "Script")
sys.path.append(name + "Optimisation")

import numpy as np
from Utils.ReadSetupFile import ReadSetupFile
import os
from ArmModel.GeometricModel import mgd


def endPosBrent():
    rs = ReadSetupFile()
    for el in os.listdir(rs.pathFolderTrajectories):
        mati = np.loadtxt(rs.pathFolderTrajectories + el)
        a = mati[mati.shape[0]-1,10]
        b = mati[mati.shape[0]-1, 11]
        junk, xy = mgd(np.array([[a], [b]]), 0.3, 0.35)
        print(xy[1])
        
