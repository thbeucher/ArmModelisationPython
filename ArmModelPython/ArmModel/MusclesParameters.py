'''
Author: Thomas Beucher

Module: MusclesParameters

Description:    -We find here all muscles parameters
                -we use a model of arm with two joints and six muscles
'''
import os
import numpy as np

class MusclesParameters:
    
    def __init__(self):
        self.fmaxMatrix()
        
    def fmaxMatrix(self):
        '''
        This function allow to define the matrix of the maximum force exerted by each muscle
        '''
        with open(os.path.realpath("Setup/setupMusclesParameters"), "r") as file:
            alls = file.read()
        allsByLign = alls.split("\n")
        #line 1, fmax1
        fmax1 = float((allsByLign[0].split(":"))[1])
        #line 2, fmax2
        fmax2 = float((allsByLign[1].split(":"))[1])
        #line 3, fmax3
        fmax3 = float((allsByLign[2].split(":"))[1])
        #line 4, fmax4
        fmax4 = float((allsByLign[3].split(":"))[1])
        #line 5, fmax5
        fmax5 = float((allsByLign[4].split(":"))[1])
        #line 6, fmax6
        fmax6 = float((allsByLign[5].split(":"))[1])
        #matrix definition
        self.fmax = np.diag([fmax1, fmax2, fmax3, fmax4, fmax5, fmax6])
        
        
mp = MusclesParameters()
print(mp.fmax)
        
        
        
        
        