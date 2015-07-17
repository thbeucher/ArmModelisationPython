#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: NextStateComputation

Description: this class permits to generate the next state from the previous state, ie state at time t+1 given state at time t
'''
import cython
from Crypto.PublicKey._slowmath import rsa_construct
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

from StateVectorUtil import getDotQAndQFromStateVectorS, createStateVector
from ArmDynamics import mdd
from GeometricModel import jointStop


cdef class NextStateComputation:

    cdef:
        str name
        object mac
        object armP
        object rs
        object musclesP
        np.ndarray state
    
    def __init__(self):
        self.name = "NextStateComputation"
        
    cpdef initParametersNSC(self, object mac, object armP, object rs, object musclesP):
        '''
        Initializes parameters used in the functions below
        
        Input:    -mac: Muscular Activation Command, class object
                    -armP: armParameters, class object
                    -rs: ReadSetup, class object
                    -musclesP: musclesParameters, class object
        '''
        self.mac = mac
        self.armP = armP
        self.rs = rs
        self.musclesP = musclesP
        
    cpdef initStateNSC(self, np.ndarray[DTYPE_t, ndim=2] state):
        self.state = state
        
    cpdef setNewStateNSC(self, np.ndarray[DTYPE_t, ndim=2] state):
        self.state = state
    
    cpdef np.ndarray[DTYPE_t, ndim=2] computeNextState(self, np.ndarray[DTYPE_t, ndim=2] U):
        '''
        Compute the state at time t+1 given the state at time t
        
        Input:    -state:the state at time t, numpy array, here the dimension is (4,1), state = [dotq1, dotq2, q1, q2]
        
        Output:    -nextState: state at time t+1, numpy array
                    -U: muscular activation vector, numpy array, here the dimension is (6,1)
        '''
        cdef:
            np.ndarray[DTYPE_t, ndim=2] dotq
            np.ndarray[DTYPE_t, ndim=2] q
            np.ndarray[DTYPE_t, ndim=2] ddotq
            np.ndarray[DTYPE_t, ndim=2] nextState
        dotq, q = getDotQAndQFromStateVectorS(self.state)
        ddotq, dotq, q = mdd(q, dotq, U, self.armP, self.musclesP, self.rs.dt)
        q = jointStop(q)
        nextState = createStateVector(dotq, q)
        self.setNewStateNSC(nextState)
        return nextState
    
    
    
    
    
