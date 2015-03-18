from math import sqrt
import numpy as np

class costFunction:
    
    def __init__(self):
        self.gamma = 0.998
        self.rho = 1
        self.ups = 3000
        self.Ju = 0
        
    def costFunctionJ(self, U, action, t):
        usquare = np.square(U)
        usum = 0
        for i in range(6):
            usum += usquare[i,0]
        mvtCost = (sqrt(usum))**2
        if action == 1:
            imReward = 0
        else:
            imReward = 1
        self.Ju += np.exp(-t/self.gamma)*(self.rho*imReward - self.ups*mvtCost)
