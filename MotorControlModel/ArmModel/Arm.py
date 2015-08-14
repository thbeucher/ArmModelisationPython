#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: Arm

Description:    
-Models an arm with two joints and six muscles
-Computes its dynamics
'''

import numpy as np
import math

from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters

# -------------------- functions ---------------------------------

def  createStateVector(dotq, q):
  '''
  Creates the state vector [dotq1, dotq2, q1, q2]
  
  Inputs:     -dotq: numpy array
              -q: numpy array
    
  Outputs:    -state: numpy array, the state vector
  '''
  state = np.array([dotq[0], dotq[1], q[0], q[1]])   #.flatten()
  return state

def getDotQAndQFromStateVector(state):
        '''
        Returns dotq and q from the state vector state
    
        Input:      -state: numpy array, state vector
    
        Outputs:    -dotq: numpy array
        -q: numpy array
        '''
        dotq = np.array([state[0], state[1]])
        q = np.array([state[2], state[3]])
        return dotq, q

def jointStop(q):
        '''
        Articular stop for the human arm
        Shoulder: -0.6 <= q1 <= 2.6
        Elbow: -0.2 <= q2 <= 3.0
    
        Inputs:    -q: (2,1) numpy array
    
        Outputs:    -q: (2,1) numpy array
        '''
        if q[0] < -0.6:
            q[0] = -0.6
        elif q[0] > 2.6:
            q[0] = 2.6
        if q[1] < -0.2:
            q[1] = -0.2
        elif q[1] > 3.0:
            q[1] = 3.0
        return q

#-----------------------------------------------------------------------------

class Arm:

  def __init__(self):
        self.__dotq0 = np.array([0.,0.])
        self.armP = ArmParameters()
        self.musclesP = MusclesParameters()
        
  def setState(self, state):
        self.state = state
        
  def setDT(self, dt):
        self.dt = dt
        
  def get_dotq_0(self):
        return np.array(self.__dotq0)

  def set_dotq_0(self, value):
        self.__dotq0 = value

  def computeNextState(self, U, state):
        '''
        Computes the next state resulting from the direct dynamic model of the arm given the muscles activation vector U
    
        Inputs:     -U: (6,1) numpy array
                   -state: (4,1) numpy array (used for Kalman, not based on the current system state)

        Output:    -state: (4,1) numpy array, the resulting state
        '''
        dotq, q = getDotQAndQFromStateVector(state)
        M = np.array([[self.armP.k1+2*self.armP.k2*math.cos(q[1]),self.armP.k3+self.armP.k2*math.cos(q[1])],[self.armP.k3+self.armP.k2*math.cos(q[1]),self.armP.k3]])
        C = np.array([-dotq[1]*(2*dotq[0]+dotq[1])*self.armP.k2*math.sin(q[1]),(dotq[0]**2)*self.armP.k2*math.sin(q[1])])
        Minv = np.linalg.inv(M)
        #the commented version uses a non null stiffness for the muscles
        #beware of dot product Kraid times q: q may not be the correct vector/matrix
        #Gamma = np.dot((np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Kraid, q)), U)
        #Gamma = np.dot((np.dot(self.armP.At, self.musclesP.fmax)-np.dot(self.musclesP.Knulle, Q)), U)
        #above Knulle is null, so it can be simplified
        Gamma = np.dot(np.dot(self.armP.At, self.musclesP.fmax), U)
        #Gamma = np.dot(armP.At, np.dot(musclesP.fmax,U))
        #computes the acceleration ddotq and integrates

        #print ("M:",M)
        #print ("C:",C)
        #print ("Gamma:",Gamma)
        #print ("dotq:",dotq)
 
        ddotq = np.dot(Minv,(Gamma - C - np.dot(self.armP.B, dotq)))

        #print ("ddotq",ddotq)

        dotq += ddotq*self.dt
        q += dotq*self.dt
        #save the real state to compute the state at the next step with the real previous state
        q = jointStop(q)
        nextState = createStateVector(dotq, q)
        return nextState
    
  def mgd(self, q):
        '''
        Direct geometric model of the arm
    
        Inputs:     -q: (2,1) numpy array
    
        Outputs:
        -coordElbow: elbow coordinate
        -coordHand: hand coordinate
        '''
        coordElbow = [self.armP.l1*np.cos(q[0]), self.armP.l1*np.sin(q[0])]
        coordHand = [self.armP.l2*np.cos(q[1] + q[0]) + self.armP.l1*np.cos(q[0]), self.armP.l2*np.sin(q[1] + q[0]) + self.armP.l1*np.sin(q[0])]
        return coordElbow, coordHand

  def mgi(self, xi, yi):
        '''
        Inverse geometric model of the arm
    
        Inputs:     -xi: abscissa of the end-effector point
                    -yi: ordinate of the end-effectior point

        Outputs:
                    -q1: arm angle
                    -q2: foreArm angle
        '''
        a = ((xi**2)+(yi**2)-(self.armP.l1**2)-(self.armP.l2**2))/(2*self.armP.l1*self.armP.l2)
        try:
            q2 = math.acos(a)
            c = self.armP.l1 + self.armP.l2*(math.cos(q2))
            d = self.armP.l2*(math.sin(q2))
            q1 = math.atan2(yi,xi) - math.atan2(d,c)
            return q1, q2
        except ValueError:
            print("forbidden value")
            return "None"    








