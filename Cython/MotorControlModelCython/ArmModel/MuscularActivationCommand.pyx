#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: MuscularActivationCommand

Description: Class used to compute the muscular activation vector U with motor noise
'''
import numpy as np

class MuscularActivationCommand:
    
    def __init__(self):
        self.name = "MuscularActivationCommand"
        
    def initParametersMAC(self, fa, rs):
        '''
    	Initializes parameters used in the functions below
    
    	Inputs:		-fa, functionApproximator, class object
    			-rs, readsetup, class object
    	'''
        self.fa = fa
        self.rs = rs
        
    def setThetaMAC(self, theta):
        '''
    	Set the theta for the rest of the class
    
    	Input:		-theta, the controller ie the vector of parameters, numpy array
    	'''
        self.theta = theta
    
    def getCommandMAC(self, state):
        '''
    	Computes the next muscular activation vector U
    
    	Input:		-state: the state of the arm, numpy array
    
    	Output:		-Unoise: the muscular activation vector U with motor noise
    	'''
        #compute the next muscular activation vector using the controller theta
        U = self.fa.computesOutput(state, self.theta)
        #add the motor noise
        UnoiseTmp = U*(1+ np.random.normal(0,self.rs.knoiseU))
        #check if the muscular activation are normed, ie between 0 and 1
        UnoiseTmp = self.checkRangeEndpoint(UnoiseTmp)
        #put U in column vector form
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    def checkRangeEndpoint(self, UnoiseTmp):
        '''
		Checks if the muscular activation is between 0 and 1
		
		Input:		-UnoiseTmp: muscular activation vector
		
		Output:		-UnoiseTmp: muscular activation vector
        '''
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        return UnoiseTmp
    
    
    
    
    
