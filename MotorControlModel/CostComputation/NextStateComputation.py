#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: NextStateComputation

Description: this class permits to generate the next state from the previous state, ie state at time t+1 given state at time t
'''

#from ArmModel.Arm import getDotQAndQFromStateVector, createStateVector

class NextStateComputation:
    
    def __init__(self):
        self.name = "NextStateComputation"
        
    def initParametersNSC(self, mac, armM, rs):
        '''
        Initializes parameters used in the functions below
        
        Input:    -mac: Muscular Activation Command, class object
                    -armM: armModel, class object
                    -rs: ReadSetup, class object
        '''
        self.mac = mac
        self.armM = armM
        self.rs = rs
        
    def setState(self, state):
        self.state = state
    
    def computeNextState(self, U):
        '''
        Compute the state at time t+1 given the state at time t
        
        Input:    -state:the state at time t, numpy array, here the dimension is (4,1), state = [dotq1, dotq2, q1, q2]
        
        Output:    -nextState: state at time t+1, numpy array
                    -U: muscular activation vector, numpy array, here the dimension is (6,1)
        '''
        dotq, q = getDotQAndQFromStateVector(self.state)
        ddotq, dotq, q = self.armM.mdd(q, dotq, U, self.rs.dt)
        q = jointStop(q)
        nextState = createStateVector(dotq, q)
        self.setNewStateNSC(nextState)
        return nextState
    
    
    
    
    
