'''
Author: Thomas Beucher

Module: UnscentedKalmanFilterControl

Description: 
'''
import numpy as np
from pykalman import UnscentedKalmanFilter

class UnscentedKalmanFilterControl:
    
    def __init__(self):
        self.name = "UnscentedKalmanFilter"
        
    def initParametersUKF(self, dimState, dimObs, delay, nsc, armD, mac):
        self.dimState = dimState
        self.dimObs = dimObs
        self.delay = delay
        self.nsc = nsc
        self.armD = armD
        self.mac = mac
        transition_covariance = np.eye(self.dimState)*0.01
        initial_state_mean = np.zeros(self.dimState)
        observation_covariance = 1000*np.eye(self.dimObs) 
        initial_state_covariance = np.eye(self.dimState)
        self.nextCovariance = np.eye(self.dimState)*0.0001
        self.ukf = UnscentedKalmanFilter(self.transitionFunctionUKF, self.observationFunctionUKF,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
    
    def setDelayUKF(self, delay):
        self.delay = delay
    
    def transitionFunctionUKF(self, stateU, transitionNoise = 0):
        nextX = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        nextStateU = self.mac.getCommandMAC(nextX)
        nextStateUNoise = nextStateU.T[0] + transitionNoise
        return nextStateUNoise
    
    def observationFunctionUKF(self, stateU, observationNoise = 0):
        nextObs = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        nextObsNoise = nextObs.T[0] + observationNoise
        return nextObsNoise
    
    def initObsStore(self, state):
        self.obsStore = np.tile(state, (1, self.delay))
    
    def storeObs(self, state):
        self.obsStore = np.roll(self.obsStore, 1, axis = 1)
        self.obsStore.T[0] = state.T
    
    def runUKF(self, stateU, obs):
        self.storeObs(obs)
        nextState, nextCovariance = self.ukf.filter_update(stateU.T[0], self.nextCovariance, self.obsStore.T[self.delay-1])
        stateApprox = self.armD.mddADUKF(np.asarray(nextState).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        return stateApprox
    
    
    
    