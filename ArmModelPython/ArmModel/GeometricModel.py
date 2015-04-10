'''
Author: Thomas Beucher

Module: InverseGeometricModel

Description: we find here the inverse and direct geometric model for a two joints arm
'''

import math
import numpy as np

def mgi(xi, yi, l1, l2):
    '''
    Inverse geometric model
        
    Inputs:    -xi: absciss of the effective point
                -yi: ordinate of the effective point
                -l1: arm length
                -l2: foreArm length
        
    Outputs:
                -q1: arm angle
                -q2: foreArm angle
    '''
    a = ((xi**2)+(yi**2)-(l1**2)-(l2**2))/(2*l1*l2)
    try:
        q2 = math.acos(a)
        c = l1 + l2*(math.cos(q2))
        d = l2*(math.sin(q2))
        q1 = math.atan2(yi,xi) - math.atan2(d,c)
        return q1, q2
    except ValueError:
        print("forbidden value")
        return "None"
    
    
def mgd(q, l1, l2):
    '''
    Direct geometric model of the arm
        
    Inputs:     -q: (2,1) numpy array
                -l1: arm length
                -l2: foreArm length
        
    Outputs:
                -q1: arm angle
                -q2: foreArm angle
    '''
    coordElbow = (l1*np.cos(q[0,0]), l1*np.sin(q[0,0]))
    coordHand = (l2*np.cos(q[1,0] + q[0,0]) + l1*np.cos(q[0,0]), l2*np.sin(q[1,0] + q[0,0]) + l1*np.sin(q[0,0]))
    return coordElbow, coordHand
    
    
def jointStop(q):
    '''
    Articular stop for the human arm
    Shoulder: -0.6 <= q1 <= 2.6
    Elbow: -0.2 <= q2 <= 3.0
    
    Inputs:    -q: (2,1) numpy array
    
    Outputs:    -q: (2,1) numpy array
    '''
    if q[0,0] < -0.6:
        q[0,0] = -0.6
    elif q[0,0] > 2.6:
        q[0,0] = 2.6
    if q[1,0] < -0.2:
        q[1,0] = -0.2
    elif q[1,0] > 3.0:
        q[1,0] = 3.0
    return q
    
    
    