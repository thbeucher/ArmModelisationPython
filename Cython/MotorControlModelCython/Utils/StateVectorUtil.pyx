#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: StateVectorUtil

Description: We find here some functions usefull to handle the state vector
'''
import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t


cpdef np.ndarray[DTYPE_t, ndim=2] createStateVector(np.ndarray[DTYPE_t, ndim=2] dotq, np.ndarray[DTYPE_t, ndim=2] q):
        '''
        Create the state vector s [dotq1, dotq2, q1, q2]
        
        Inputs:     -dotq: numpy array
                    -q: numpy array
        
        Outputs:    -inputQ: numpy array, the state vector
        '''
        cdef np.ndarray[DTYPE_t, ndim=2] inputQ
        inputQ = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
        return inputQ
    
cpdef tuple getDotQAndQFromStateVectorS(np.ndarray[DTYPE_t, ndim=2] inputQ):
    '''
    Return dotq and q from the state vector inputQ
        
    Input:      -inputQ: numpy array, state vector
        
    Outputs:    -dotq: numpy array
                -q: numpy array
    '''
    cdef:
        np.ndarray[DTYPE_t, ndim=2] dotq
        np.ndarray[DTYPE_t, ndim=2] q
    dotq = np.array([[inputQ[0,0]], [inputQ[1,0]]])
    q = np.array([[inputQ[2,0]], [inputQ[3,0]]])
    return dotq, q
