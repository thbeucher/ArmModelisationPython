'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: 
'''
import numpy as np

class CostComputation:
    
    def __init__(self):
        self.name = "CostComputation"
        
    def initParametersCC(self, rs):
        self.rs = rs
        
    def computeStateTransitionCost(self, cost, U, t):
        mvtCost = (np.linalg.norm(U))**2
        cost += np.exp(-t/self.rs.gammaCF)*(-self.rs.upsCF*mvtCost)
        return cost
    
    def computeFinalCostReward(self, cost, t):
        cost += np.exp(-t/self.rs.gammaCF)*self.rs.rhoCF
        return cost
    
    
    
    
    
