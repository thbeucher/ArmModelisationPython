'''
Author: Thomas Beucher

Module: ArmDynamics

Description:    -We find here all dynamics of the arm
                -we use a model of arm with two joints and six muscles
'''
import numpy as np
import math

class ArmDynamics:
    
    def __init__(self):
        self.__dotq0 = np.array([[0.],[0.]])

    def get_dotq_0(self):
        return np.array(self.__dotq0)


    def set_dotq_0(self, value):
        self.__dotq0 = value


    def del_dotq_0(self):
        del self.__dotq0

    dotq0 = property(get_dotq_0, set_dotq_0, del_dotq_0, "dotq0's docstring")
    


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
    C = np.array([[-dotq[1,0]*(2*dotq[0,0]+dotq[1,0])*armP.k2*math.sin(q[1,0])],[(dotq[0,0]**2)*armP.k2*math.sin(q[1,0])]])
    #inversion of M
    Minv = np.linalg.inv(M)
    #torque term
    Q = np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])
    #Gamma = np.dot((np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Kraid, Q)), U)
    Gamma = np.dot((np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Knulle, Q)), U)
    #Gamma = np.dot(armP.At, np.dot(musclesP.fmax,U))
    #computation of ddotq
    ddotq = np.dot(Minv,(Gamma - C - np.dot(armP.B, dotq)))
    return ddotq

def integration(dotq, q, ddotq, dt):
    '''
    This function compute dotq and q from ddotq
    
    Inputs:     -ddotq: (2,1) numpy array
                -dt: scalar
    
    Outputs:    -dotq: (2,1) numpy array
                -q: (2,1) numpy array
    '''
    dotq += ddotq*dt
    q += dotq*dt
    return dotq, q
    
    
    
    
    
    
    
    