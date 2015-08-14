#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: MuscularActivation

Description: Class used to compute the muscular activation vector U with motor noise
'''
import numpy as np
    
def getNoisyCommand(U, knoiseU):
    '''
    Computes the next muscular activation vector U
    
    Input:		-state: the state of the arm, numpy array
    
    Output:		-Unoise: the muscular activation vector U with motor noise
    '''
    #add the motor noise
    UnoiseTmp = U*(1+ np.random.normal(0,knoiseU))
    #check if the muscular activation are normed, ie between 0 and 1
    UnoiseTmp = checkRangeEndpoint(UnoiseTmp)
    #put U in column vector form
    Unoise = np.array([UnoiseTmp]).T
    return Unoise
        
def checkRangeEndpoint(UnoiseTmp):
    '''
    Makes sure that the muscular activation is between 0 and 1
    
    Input:		-UnoiseTmp: muscular activation vector
		
    Output:		-UnoiseTmp: muscular activation vector
    '''
    for i in range(UnoiseTmp.shape[0]):
       if UnoiseTmp[i] < 0:
            UnoiseTmp[i] = 0
       elif UnoiseTmp[i] > 1:
            UnoiseTmp[i] = 1
    return UnoiseTmp
    
    
    
    
