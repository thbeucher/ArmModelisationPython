#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: UnscentedKalmanFilterControl

Description: Class with some functions to use the unscented kalman filter to generate trajectories and reproduced the human control motor delay.
Uses the librairy pykalman.
'''
import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

from pykalman import UnscentedKalmanFilter

cdef class UnscentedKalmanFilterControl:

    cdef:
        str name
        int dimState
        int dimObs
        int delay
        public object nsc
        object armD
        object mac
        np.ndarray nextCovariance
        object ukf
        np.ndarray obsStore
    
    def __init__(self):
        self.name = "UnscentedKalmanFilter"
        
    cpdef initParametersUKF(self, int dimState, int dimObs, int delay, object nsc, object armD, object mac):
        '''
    	Initializes parameters to uses the function implemented below
    	
    	inputs:		-dimState: dimension of the state, here the state correspond to the muscular activation vector U, int
    			-dimObs: dimension of the observation, here the observation is the position of the arm given by the model, int
    			-delay: the delay with which we give the observation to the filter, int
    			-nsc, nextStateComputation, class object
    			-armD, armDynamics, class object
    			-mac, MuscularActivationCommand
    	'''
        cdef:
            np.ndarray[DTYPE_t, ndim=2] transition_covariance
            np.ndarray[DTYPE_t, ndim=1] initial_state_mean
            np.ndarray[DTYPE_t, ndim=2] observation_covariance
            np.ndarray[DTYPE_t, ndim=2] initial_state_covariance
        self.dimState = dimState
        self.dimObs = dimObs
        self.delay = delay
        self.nsc = nsc
        self.armD = armD
        self.mac = mac
        #initialization of some parameters for the filter
        transition_covariance = np.eye(self.dimState)*0.01
        initial_state_mean = np.zeros(self.dimState)
        observation_covariance = 1000*np.eye(self.dimObs) 
        initial_state_covariance = np.eye(self.dimState)
        self.nextCovariance = np.eye(self.dimState)*0.0001
        self.ukf = UnscentedKalmanFilter(self.transitionFunctionUKF, self.observationFunctionUKF,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
    
    cpdef setDelayUKF(self, int delay):
        '''
    	Sets the delay used for the filter
    	
    	Input:		-delay, int
    	'''
        self.delay = delay
    
    cpdef np.ndarray[DTYPE_t, ndim=1] transitionFunctionUKF(self, np.ndarray stateU, np.ndarray transitionNoise):
        '''
    	Transition function used by the filter, function of the state and the transition noise at time t and produces the state at time t+1
    	
    	Inputs:		-stateU: the state at time t, numpy array
    			-transitionNoise: transition noise at time t, numpy array
    
    	Output:		-nextStateUNoise: the next State with noise added, numpy array
    	'''
        cdef:
            np.ndarray[DTYPE_t, ndim=2] nextX
            np.ndarray[DTYPE_t, ndim=2] nextStateU
            np.ndarray[DTYPE_t, ndim=1] nextStateUNoise
        #computation of the next Q vector [dotq1, dotq2, q1, q2]
        nextX = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        #computation of the next muscular activation vector U
        nextStateU = self.mac.getCommandMAC(nextX)
        #noise add to the next state generated
        nextStateUNoise = nextStateU.T[0] + transitionNoise
        return nextStateUNoise
    
    cpdef np.ndarray[DTYPE_t, ndim=1] observationFunctionUKF(self, np.ndarray stateU, np.ndarray observationNoise):
        '''
    	Observation function used by the filter, function of the state and the observation noise at time t and produces the observation at time t
    
    	Inputs:		-stateU: the state at time t, numpy array
    			-observationNoise: the observation noise at time t, numpy array
    
    	Output:		-nextObsNoise: observation at time t+1
    	'''
        cdef:
            np.ndarray[DTYPE_t, ndim=2] nextObs
            np.ndarray[DTYPE_t, ndim=1] nextObsNoise
        #computation of the next observation
        nextObs = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        nextObsNoise = nextObs.T[0] + observationNoise
        return nextObsNoise
    
    cpdef initObsStore(self, np.ndarray[DTYPE_t, ndim=2] state):
        '''
    	Initialization of the observation storage
    
    	Input:		-state: the state to store in order to create the delay wanted
    	'''
        self.obsStore = np.tile(state, (1, self.delay))
    
    cpdef storeObs(self, np.ndarray[DTYPE_t, ndim=2] state):
        '''
    	Stores the state to create the delay wanted
    
    	Input:		-state: the state to store
    	'''
        self.obsStore = np.roll(self.obsStore, 1, axis = 1)
        self.obsStore.T[0] = state.T
    
    cpdef np.ndarray[DTYPE_t, ndim=2] runUKF(self, np.ndarray[DTYPE_t, ndim=2] stateU, np.ndarray[DTYPE_t, ndim=2] obs):
        '''
    	Function used to compute the next state approximation with the filter
    
    	Inputs:		-stateU: the state to feed the filter, here its the muscular activation vector U, numpy array of dimension (x, 1), here x = 6
    			    -obs: the observation of the arm position, numpy array of dimension (x, 1), here x = 4
    
    	Output:		-stateApprox: the next state approximation, numpy array of dimension (x, 1), here x = 4
    	'''
        cdef:
            np.ndarray nextState
            np.ndarray nextCovariance
            np.ndarray[DTYPE_t, ndim=2] stateApprox
        #store the state of the arm to feed the filter with a delay on the observation
        self.storeObs(obs)
        #compute the nextState approximation ie here the next muscular activation
        nextState, nextCovariance = self.ukf.filter_update(stateU.T[0], self.nextCovariance, self.obsStore.T[self.delay-1])
        #compute the nextState ie the next position vector from the approximation of the next muscular activation vector given by the filter
        stateApprox = self.armD.mddADUKF(np.asarray(nextState).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        return stateApprox
    
    
    
    
