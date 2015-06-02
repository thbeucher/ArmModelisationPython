'''
Author: Thomas Beucher

Module: KalmanModule

Description: Here the implementation of the Unscented Kalman filter module
'''
import numpy as np
from pykalman import UnscentedKalmanFilter

class KalmanModule:
    
    def __init__(self, NS):
        self.name = "KalmanModule"
        self.delay = 3
        self.NS = NS
        
    def kalmanFilterInit(self, dimState):
        '''
        Initializes components for the Unscented Kalman filter
        '''
        transition_covariance = np.eye(dimState)
        initial_state_mean = np.zeros(dimState)
        random_state =np.random.RandomState(0)
        observation_covariance = np.eye(dimState) + random_state.randn(dimState,dimState) * 0.1
        initial_state_covariance = [[1, 0.1], [-0.1, 1]]#A revoir
        ukf = UnscentedKalmanFilter(self.transition_function, self.observation_function,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance,
                                    random_state = random_state)
        return ukf, initial_state_covariance
        
    def transition_function(self, state, noise = 0):
        '''
        transition_functions[t] is a function of the state and the transition noise at time t 
        and produces the state at time t+1
        
        Input:     -inputQ: numpy array (state_dimension, ), the state vector s at time t (dotq1, dotq2, q1, q2)
        
        Output:    -outputQ: numpy array (state_dimension, ), the state vector at time t+1
        '''
        nextState, Utransi = self.NS.computeNextState(state[0])
        nextStateNoise = nextState + noise
        return nextStateNoise
    
    def observation_function(self, inputQ, noise = 0):
        '''
        observation_functions[t] is a function of the state and the observation noise at time t 
        and produces the observation at time t
        '''
        nextState, Uobs = self.NS.computeNextState(inputQ[self.delay-1])
        nexStateNoise = nextState + noise
        return nexStateNoise    
    
