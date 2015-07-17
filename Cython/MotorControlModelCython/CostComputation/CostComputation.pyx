#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: The class which computes the trajectory cost
'''
import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t


cdef class CostComputation:

    cdef:
        str name
        object rs
    
    def __init__(self):
        self.name = "CostComputation"
        
    cpdef initParametersCC(self, object rs):
        '''Initializes class object needed to acces to the setup variables
        
        Input:	-rs: ReadSetup, class object given acces to the setup variables
        '''
        self.rs = rs
        
    cpdef double computeStateTransitionCost(self, double cost, np.ndarray[DTYPE_t, ndim=2] U, double t):
        '''
		Computes the cost on one step of the trajectory
		
		Input:	-cost: cost at time t, float
				-U: muscular activation vector, numpy array (6,1)
				-t: time, float
				
		Output:		-cost: cost at time t+1, float
		'''
        cdef double mvtCost
        #compute the square of the norm of the muscular activation vector
        mvtCost = (np.linalg.norm(U))**2
        #compute the cost following the law of the model
        cost += np.exp(-t/self.rs.gammaCF)*(-self.rs.upsCF*mvtCost)
        return cost
    
    cpdef double computeFinalCostReward(self, double cost, double t):
        '''
		Computes the cost on final step if the target is reached
		
		Input:		-cost: cost at the end of the trajectory, float
					-t: time, float
					
		Output:		-cost: final cost if the target is reached
		'''
        cost += np.exp(-t/self.rs.gammaCF)*self.rs.rhoCF
        return cost
    
    
    
    
    
