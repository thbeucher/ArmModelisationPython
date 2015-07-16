#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: ArmDynamics

Description:    
-Models an arm with two joints and six muscles
-Computes its dynamics
'''

import numpy as np
import math
from StateVectorUtil import createStateVector, getDotQAndQFromStateVectorS

class ArmDynamics:
    
    def __init__(self):
        self.__dotq0 = np.array([[0.],[0.]])
        
    def initStateAD(self, state):
        self.state = state
        
    def initParametersAD(self, armP, musclesP, dt):
        self.armP = armP
        self.musclesP = musclesP
        self.dt = dt
        
    def setNewStateAD(self, dotq, q):
        self.state = createStateVector(dotq, q)
        
    def computeMCQ(self, state):
        '''
        Sets M, C, Minv, Q to compute the dynamic equation of the arm
        
        Inputs:     -state: (4,1) numpy array
                    -dotq: (2,1) numpy array
                    -q: (2,1) numpy array

        Output:    -Minv: inverse inertia matrix, numpy array
                    -C: coriolis force vector, numpy array
                    -Q: torque term, numpy array
        '''
        dotq, q = getDotQAndQFromStateVectorS(state)
        M = np.array([[self.armP.k1+2*self.armP.k2*math.cos(q[1,0]),self.armP.k3+self.armP.k2*math.cos(q[1,0])],[self.armP.k3+self.armP.k2*math.cos(q[1,0]),self.armP.k3]])
        C = np.array([[-dotq[1,0]*(2*dotq[0,0]+dotq[1,0])*self.armP.k2*math.sin(q[1,0])],[(dotq[0,0]**2)*self.armP.k2*math.sin(q[1,0])]])
        Minv = np.linalg.inv(M)
        Q = np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])
        return Minv, C, Q, dotq, q
        
    def mddAD(self, U):
        '''
        Computes the direct dynamic model of the arm given the arm state (q,dotq), the muscles parameters (armP,musclesP), the muscles activation vector U and the time step dt.
        
        Inputs:     -U: (6,1) numpy array

        Output:    -state: (4,1) numpy array
        '''
        Minv, C, Q = self.computeMCQ(self.state)
        #the commented version uses a non null stiffness for the muscles
        #Gamma = np.dot((np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Kraid, Q)), U)
        Gamma = np.dot((np.dot(self.armP.At, self.musclesP.fmax)-np.dot(self.musclesP.Knulle, Q)), U)
        #Gamma = np.dot(armP.At, np.dot(musclesP.fmax,U))
        #computes the acceleration ddotq and integrates
        dotq, q = getDotQAndQFromStateVectorS(self.state)
        ddotq = np.dot(Minv,(Gamma - C - np.dot(self.armP.B, dotq)))
        dotq += ddotq*self.dt
        q += dotq*self.dt
        #save the real state to compute the state at the next step with the real previous state
        self.setNewStateAD(dotq, q)
        return self.state
    
    def mddADUKF(self, U, state):
        '''
        Computes the next state for the kalman filter
        
        Inputs:     -U: (6,1) numpy array
                    -state: (4,1) numpy array

        Output:    -nextState: (4,1) numpy array
        '''
        Minv, C, Q, dotq, q = self.computeMCQ(state)
        Gamma = np.dot((np.dot(self.armP.At, self.musclesP.fmax)-np.dot(self.musclesP.Knulle, Q)), U)
        ddotq = np.dot(Minv,(Gamma - C - np.dot(self.armP.B, dotq)))
        dotq += ddotq*self.dt
        q += dotq*self.dt
        nextState = createStateVector(dotq, q)
        return nextState

    def get_dotq_0(self):
        return np.array(self.__dotq0)


    def set_dotq_0(self, value):
        self.__dotq0 = value


    def del_dotq_0(self):
        del self.__dotq0

    dotq0 = property(get_dotq_0, set_dotq_0, del_dotq_0, "dotq0's docstring")
    

def mdd(q, dotq, U, armP, musclesP, dt):
    '''
    Computes the direct dynamic model of the arm given the arm state (q,dotq), the muscles parameters (armP,musclesP), the muscles activation vector U and the time step dt.
    
    Inputs:     -q: (2,1) numpy array
                -dotq: (2,1) numpy array
                -U: (6,1) numpy array
                -armP: class object
                -musclesP: class object
    Output:    -ddotq: (2,1) numpy array
    '''
    #Inertia matrix
    M = np.array([[armP.k1+2*armP.k2*math.cos(q[1,0]),armP.k3+armP.k2*math.cos(q[1,0])],[armP.k3+armP.k2*math.cos(q[1,0]),armP.k3]])
    #Coriolis force vector
    C = np.array([[-dotq[1,0]*(2*dotq[0,0]+dotq[1,0])*armP.k2*math.sin(q[1,0])],[(dotq[0,0]**2)*armP.k2*math.sin(q[1,0])]])
    #inversion of M
    Minv = np.linalg.inv(M)
    #torque term
    Q = np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])
    #the commented version uses a non null stiffness for the muscles
    #Gamma = np.dot((np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Kraid, Q)), U)
    Gamma = np.dot((np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Knulle, Q)), U)
    #Gamma = np.dot(armP.At, np.dot(musclesP.fmax,U))
    #computes the acceleration ddotq and integrates
    ddotq = np.dot(Minv,(Gamma - C - np.dot(armP.B, dotq)))
    dotq += ddotq*dt
    q += dotq*dt
    return ddotq, dotq, q

    
    
    
    
    
    
    
    
