'''
Author: Thomas Beucher

Module: NextStateComputation

Description: 
'''
from Utils.StateVectorUtil import getDotQAndQFromStateVectorS, createStateVector
from ArmModel.ArmDynamics import mdd
from ArmModel.GeometricModel import jointStop

#Thomas: to be commented
#Thomaas: put together with CostComputation?

class NextStateComputation:
    
    def __init__(self):
        self.name = "NextStateComputation"

#why NSC?
        
    def initParametersNSC(self, mac, armP, rs, musclesP):
        self.mac = mac
        self.armP = armP
        self.rs = rs
        self.musclesP = musclesP
    
    def computeNextState(self, state):
        U = self.mac.getCommandMAC(state)
        dotq, q = getDotQAndQFromStateVectorS(state)
        ddotq, dotq, q = mdd(q, dotq, U, self.armP, self.musclesP, self.rs.dt)
        q = jointStop(q)
        nextState = createStateVector(dotq, q)
        return nextState, U
    
    
    
    
    
