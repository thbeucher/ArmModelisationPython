#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: InverseGeometricModel

Description: we find here the inverse and direct geometric model for a two joints arm and also the joint stop function 
                for the human arm
'''
import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

import math

def mgi(xi, yi, l1, l2):
    '''
    Inverse geometric model
        
    Inputs:     -xi: abscissa of the end-effector point
                -yi: ordinate of the end-effectior point
                -l1: arm length
                -l2: foreArm length
        
    Outputs:
                -q1: arm angle
                -q2: foreArm angle
    '''
    a = ((xi**2)+(yi**2)-(l1**2)-(l2**2))/(2*l1*l2)
    try:
        q2 = math.acos(a)
        c = l1 + l2*(math.cos(q2))
        d = l2*(math.sin(q2))
        q1 = math.atan2(yi,xi) - math.atan2(d,c)
        return q1, q2
    except ValueError:
        print("forbidden value")
        return "None"
    
    
cpdef tuple mgd(np.ndarray[DTYPE_t, ndim=2] q, double l1, double l2):
    '''
    Direct geometric model of the arm
        
    Inputs:     -q: (2,1) numpy array
                -l1: arm length
                -l2: foreArm length
        
    Outputs:
                -coordElbow: elbow coordinate
                -coordHand: hand coordinate
    '''
    cdef:
        tuple coordElbow
        tuple coordHand
    coordElbow = (l1*np.cos(q[0,0]), l1*np.sin(q[0,0]))
    coordHand = (l2*np.cos(q[1,0] + q[0,0]) + l1*np.cos(q[0,0]), l2*np.sin(q[1,0] + q[0,0]) + l1*np.sin(q[0,0]))
    return coordElbow, coordHand
    
    
cpdef np.ndarray[DTYPE_t, ndim=2] jointStop(np.ndarray[DTYPE_t, ndim=2] q):
    '''
    Articular stop for the human arm
    Shoulder: -0.6 <= q1 <= 2.6
    Elbow: -0.2 <= q2 <= 3.0
    
    Inputs:    -q: (2,1) numpy array
    
    Outputs:    -q: (2,1) numpy array
    '''
    if q[0,0] < -0.6:
        q[0,0] = -0.6
    elif q[0,0] > 2.6:
        q[0,0] = 2.6
    if q[1,0] < -0.2:
        q[1,0] = -0.2
    elif q[1,0] > 3.0:
        q[1,0] = 3.0
    return q



