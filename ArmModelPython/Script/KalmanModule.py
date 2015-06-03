'''
Author: Thomas Beucher

Module: KalmanModule

Description: Here the implementation of the Unscented Kalman filter module
'''
import numpy as np
from pykalman import UnscentedKalmanFilter
from ArmModel.GeometricModel import mgd
from Utils.GenerateTrajectoryUtils import getDotQAndQFromStateVectorS

class KalmanModule:
    
    def __init__(self, NS, state, name, armP):
        self.name = "KalmanModule"
        self.delay = 3
        self.dimState = 4
        self.NS = NS
        self.state_store = np.tile(state, (1, self.delay))
        self.nameToSave = name
        self.armP = armP
        self.saveAllCoord = {}
        self.saveAllCoord[name] = []
        self.kalmanFilterInit()
        
        
    def kalmanFilterInit(self):
        '''
        Initializes components for the Unscented Kalman filter
        '''
        transition_covariance = np.eye(self.dimState)
        initial_state_mean = np.zeros(self.dimState)
        random_state =np.random.RandomState(0)
        #observation_covariance = np.eye(self.dimState) + random_state.randn(self.dimState,self.dimState) * 0.001
        #initial_state_covariance = np.asarray([[1, 0.001, 0.001, 0.001], [-0.001, 1, 0.001, 0.001], [-0.001, -0.001, 1, 0.001], [-0.001, -0.001, -0.001, 1]])
        observation_covariance = np.eye(self.dimState) + np.random.normal(0, 0.2, (self.dimState, self.dimState))
        initial_state_covariance = np.eye(self.dimState)
        self.nextCovariance = initial_state_covariance
        self.ukf = UnscentedKalmanFilter(self.transition_function, self.observation_function,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance,
                                    random_state = random_state)
        
    def transition_function(self, state, noise = 0):
        '''
        transition_functions[t] is a function of the state and the transition noise at time t 
        and produces the state at time t+1
        
        Input:     -inputQ: numpy array (state_dimension, ), the state vector s at time t (dotq1, dotq2, q1, q2)
        
        Output:    -outputQ: numpy array (state_dimension, ), the state vector at time t+1
        '''
        nextState, Utransi = self.NS.computeNextState(np.asarray([state]).T)
        nextStateNoise = nextState + np.asarray([noise]).T
        return nextStateNoise.T[0]
    
    def observation_function(self, inputQ, noise = 0):
        '''
        observation_functions[t] is a function of the state and the observation noise at time t 
        and produces the observation at time t
        '''
        if len(inputQ.shape) == 1:
            inputQ = np.asarray([inputQ]).T
        nextState, Uobs = self.NS.computeNextState(inputQ)
        nexStateNoise = nextState + np.asarray([noise]).T
        return nexStateNoise.T[0]
    
    def obs_fun_test(self, state, noise):
        pass
    
    def storeState(self, state):
        '''
        Store the state from t-delay to t
        '''
        self.state_store = np.roll(self.state_store, 1, axis = 1)
        self.state_store.T[0] = state.T
        
    def saveState(self):
        dotq, q = getDotQAndQFromStateVectorS(np.asarray([self.nextState]).T)
        junk, coordPE = mgd(q, self.armP.l1, self.armP.l2)
        self.saveAllCoord[self.nameToSave].append(coordPE)
        
    def runKalman(self, state):
        self.storeState(state)
        #print("state", state.T[0])
        #observation = self.observation_function(np.asarray([self.state_store.T[self.delay-1]]).T)
        #obs = self.transition_function(state.T[0],)
        #print("obs", obs)
        self.nextState, self.nextCovariance = self.ukf.filter_update(self.state_store.T[1], self.nextCovariance, state.T[0])
        #print("ici", self.nextState)
        #c = input("cc")
        self.saveState()
        
        
        
