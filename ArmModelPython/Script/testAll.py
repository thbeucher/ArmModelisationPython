'''
Author: Thomas Beucher

Module: testAll

Description: 
'''
from ArmModel.GeometricModel import mgi, mgd, jointStop
from Utils.CreateVectorUtil import createVector
from Utils.GenerateTrajectoryUtils import createStateVector
from Regression.functionApproximator_RBFN import fa_rbfn
import numpy as np
from Utils.StateVectorUtil import getDotQAndQFromStateVectorS
from ArmModel.ArmDynamics import mdd


def initController(rs, fr):
    fa = fa_rbfn(rs.numfeats)
    state, command = fr.getData(rs.pathFolderTrajectories)
    stateAll, commandAll = fr.dicToArray(state), fr.dicToArray(command)
    fa.setTrainingData(stateAll.T, commandAll.T)
    fa.setCentersAndWidths()
    return fa

class TrajectoriesGenerator:
    
    def __init__(self):
        self.name = "TrajectoriesGenerator"
        self.call = 0
        self.saveCost = []
        
    def initParameters(self, rs, numberOfRepeat, tg):
        self.rs = rs
        self.numberOfRepeat = numberOfRepeat
        self.tg = tg
        self.posIni = self.fr.getobjread(self.rs.experimentFilePosIni)
    
    def runTrajectories(self):
        pass
    
    def runTrajectoriesCMAWithoutParallelization(self, theta):
        costAll = [[self.tg.runTrajectory(xy[0], xy[1]) for xy in self.posIni] for i in range(self.numberOfRepeat)]
        meanByTraj = np.mean(np.asarray(costAll).reshape((self.numberOfRepeat, len(self.posIni))), axis = 0)    
        meanAll = np.mean(meanByTraj)
        self.saveCost.append(meanAll)
        print("Call n°: ", self.call, "\nCost: ", meanAll)
        self.call += 1
        return meanAll*(-1)
    
    def runTrajectoriesCMAWithParallelization(self, theta):
        pass

class TrajectoryGenerator:
    
    def __init__(self):
        self.name = "TrajectoryGenerator"
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget):
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
    
    def runTrajectory(self, x, y):
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = createVector(q1, q2)
        dotq = createVector(0., 0.)
        state = createStateVector(dotq, q)
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        i, t, cost = 0, 0, 0
        while coordHand[1] <= self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                state, U = self.nsc.computeNextState(state)
                cost = self.cc.computeStateTransitionCost(cost, U, t)
                dotq, q = getDotQAndQFromStateVectorS(state)
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
            else:
                break
            i += 1
            t = self.rs.dt
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
        return cost
            
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
        cost += np.exp(-self.t/self.rs.gammaCF)*self.rs.rhoCF
        return cost

class NextStateComputation:
    
    def __init__(self):
        self.name = "NextStateComputation"
        
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
    
class MuscularActivationCommand:
    
    def __init__(self):
        self.name = "MuscularActivationCommand"
        
    def initParametersMAC(self, theta, fa, rs):
        self.theta = theta
        self.fa = fa
        self.rs = rs
    
    def getCommandMAC(self, state):
        U = self.fa.computesOutput(state, self.theta)
        UnoiseTmp = U*(1+ np.random.normal(0,self.rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    
class UnscentedKalmanFilter:
    
    def __init__(self):
        self.name = "UnscentedKalmanFilter"
        
    def initParametersUKF(self, dimState, dimObs, delay):
        self.dimState = dimState
        self.dimObs = dimObs
        self.delay = delay
        transition_covariance = np.eye(self.dimState)*0.01
        initial_state_mean = np.zeros(self.dimState)
        observation_covariance = 1000*np.eye(self.dimObs) 
        initial_state_covariance = np.eye(self.dimState)
        self.nextCovariance = np.eye(self.dimState)*0.1
        self.ukf = UnscentedKalmanFilter(self.transition_function, self.observation_function,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
    
    def transitionFunctionUKF(self, state, transitionNoise):
        pass
    
    def observationFunctionUKF(self, state, observationNoise):
        obs = np.asarray([state[2, 0], state[3, 0]])
        obsNoise = obs + observationNoise
        return obsNoise
    
    def initStateStore(self, state):
        self.stateStore = np.tile(state, (1, self.delay))
    
    def storeState(self, state):
        self.stateStore = np.roll(self.stateStore, 1, axis = 1)
        self.stateStore.T[0] = state.T
    
    def runUKF(self):
        pass
        
        
        