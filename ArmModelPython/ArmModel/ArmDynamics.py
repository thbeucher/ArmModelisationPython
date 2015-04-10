'''
Author: Thomas Beucher

Module: MusclesParameters

Description:    -We find here all dynamics of the arm
                -we use a model of arm with two joints and six muscles
'''
import numpy as np
import math
from xml.sax.handler import DTDHandler

class ArmDynamics:
    
    def __init__(self):
        self.dotq0 = np.array([[0.],[0.]])
    


def mdd(q, dotq, U, armP, musclesP):
    '''
    This function correspond to the direct dynamic model of the arm
    
    Inputs:     -q: (2,1) numpy array
                -dotq: (2,1) numpy array
                -U: (6,1) numpy array
                -armP: class object
                -musclesP: class object
    Output:    -ddotq: (2,1) numpy array
    '''
    #Inertia matrix
    M = np.array([[armP.k1+2*armP.k2*math.cos(q[1,0]),armP.k3+armP.k2*math.cos(q[1,0])],[armP.k3+armP.k2*math.cos(q[1,0]),armP.k3]])
    #coriolis force vector
    C = np.array([[-(2*dotq[0,0]+dotq[1,0])*armP.k2*math.sin(q[1,0])],[(dotq[0,0]**2)*armP.k2*math.sin(q[1,0])]]).T
    #inversion of M
    Minv = np.linalg.pinv(M)
    #torque term
    Q = np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])
    Gamma = (np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Kraid, Q))*U
    #computation of ddotq
    ddotq = Minv*(Gamma - C - np.dot(armP.B, dotq))
    return ddotq

def integration(ddotq, dt):
    dotq = ddotq*dt
    q = dotq*dt
    return dotq, q
    
    
    
    
    
    
    
    