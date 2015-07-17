#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: MuscularActivationCommand

Description: Class used to compute the muscular activation vector U with motor noise
'''
import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

cdef class MuscularActivationCommand:

    cdef:
        str name
        object fa
        object rs
        np.ndarray theta
    
    def __init__(self):
        self.name = "MuscularActivationCommand"
        
    cpdef initParametersMAC(self, object fa, object rs):
        '''
    	Initializes parameters used in the functions below
    
    	Inputs:		-fa, functionApproximator, class object
    			-rs, readsetup, class object
    	'''
        self.fa = fa
        self.rs = rs
        
    cpdef setThetaMAC(self, np.ndarray[DTYPE_t, ndim=2] theta):
        '''
    	Set the theta for the rest of the class
    
    	Input:		-theta, the controller ie the vector of parameters, numpy array
    	'''
        self.theta = theta
    
    cpdef np.ndarray[DTYPE_t, ndim=2] getCommandMAC(self, np.ndarray[DTYPE_t, ndim=2] state):
        '''
    	Computes the next muscular activation vector U
    
    	Input:		-state: the state of the arm, numpy array
    
    	Output:		-Unoise: the muscular activation vector U with motor noise
    	'''
        cdef:
            np.ndarray[DTYPE_t, ndim=1] U
            np.ndarray[DTYPE_t, ndim=1] UnoiseTmp
            np.ndarray[DTYPE_t, ndim=2] Unoise
        #compute the next muscular activation vector using the controller theta
        U = self.fa.computesOutput(state, self.theta)
        #add the motor noise
        UnoiseTmp = U*(1+ np.random.normal(0,self.rs.knoiseU))
        #check if the muscular activation are normed, ie between 0 and 1
        UnoiseTmp = self.checkRangeEndpoint(UnoiseTmp)
        #put U in column vector form
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    cpdef np.ndarray[DTYPE_t, ndim=1] checkRangeEndpoint(self, np.ndarray[DTYPE_t, ndim=1] UnoiseTmp):
        '''
		Checks if the muscular activation is between 0 and 1
		
		Input:		-UnoiseTmp: muscular activation vector
		
		Output:		-UnoiseTmp: muscular activation vector
        '''
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        return UnoiseTmp
    
    
    
    
    
