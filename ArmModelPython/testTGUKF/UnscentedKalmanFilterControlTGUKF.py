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
        
    def initParametersUKF(self, dimState, dimObs, delay, nsc):
        self.dimState = dimState
        self.dimObs = dimObs
        self.delay = delay
        self.nsc = nsc
        transition_covariance = np.eye(self.dimState)*0.01
        initial_state_mean = np.zeros(self.dimState)
        observation_covariance = 1000*np.eye(self.dimObs) 
        initial_state_covariance = np.eye(self.dimState)
        self.nextCovariance = np.eye(self.dimState)*0.1
        self.ukf = UnscentedKalmanFilter(self.transitionFunctionUKF, self.observationFunctionUKF,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
    
    def transitionFunctionUKF(self, state, transitionNoise = 0):
        nextState, U = self.nsc.computeNextState(np.asarray(state).reshape((self.dimState, 1)))
        nextState = nextState.T[0]
        nextStateNoise = nextState + transitionNoise
        return nextStateNoise
    
    def observationFunctionUKF(self, state, observationNoise = 0):
        obs = np.asarray([state[2], state[3]])
        obsNoise = obs + observationNoise
        return obsNoise
    
    def initStateStore(self, state):
        self.stateStore = np.tile(state, (1, self.delay))
    
    def storeState(self, state):
        self.stateStore = np.roll(self.stateStore, 1, axis = 1)
        self.stateStore.T[0] = state.T
    
    def getObservation(self, state):
        return np.asarray([state[2, 0], state[3, 0]])
    
    '''def endRoutineUKF(self, state):
        #In progress
        dotq, q = getDotQAndQFromStateVectorS(state)
        coordElbow, coordHand = mgd(q, self.nsc.armP.l1, self.nsc.armP.l2)
        nextState = state
        observation = self.getObservation(state)
        while coordHand[1] < self.nsc.rs.targetOrdinate:
            nextState, nextCovariance = self.ukf.filter_update(nextState, self.nextCovariance, observation)
            dotq, q = getDotQAndQFromStateVectorS(state)
            coordElbow, coordHand = mgd(q, self.nsc.armP.l1, self.nsc.armP.l2)'''
    
    def runUKF(self, state):
        self.storeState(state)
        observation = self.getObservation(state)
        nextState, nextCovariance = self.ukf.filter_update(self.stateStore.T[self.delay-1], self.nextCovariance, observation)
        return np.asarray(nextState).reshape((self.dimState, 1))
    
    
    
    