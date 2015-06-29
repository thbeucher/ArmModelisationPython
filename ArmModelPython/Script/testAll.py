'''
Author: Thomas Beucher

Module: testAll

Description: 
'''
import cma
import numpy as np
from pykalman import UnscentedKalmanFilter
from ArmModel.GeometricModel import mgi, mgd, jointStop
from Utils.CreateVectorUtil import createVector
from Utils.GenerateTrajectoryUtils import createStateVector
from Regression.functionApproximator_RBFN import fa_rbfn
from Utils.StateVectorUtil import getDotQAndQFromStateVectorS
from ArmModel.ArmDynamics import mdd
from Utils.ThetaNormalization import normalizationNP, matrixToVector, unNormNP
from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters
from Utils.InitUtil import initFRRS


def initController(rs, fr):
    fa = fa_rbfn(rs.numfeats)
    state, command = fr.getData(rs.pathFolderTrajectories)
    stateAll, commandAll = fr.dicToArray(state), fr.dicToArray(command)
    fa.setTrainingData(stateAll.T, commandAll.T)
    fa.setCentersAndWidths()
    return fa

def initAllUsefullObj(sizeOfTarget, fr, rs):
    fa = initController(rs, fr)
    mac = MuscularActivationCommand()
    mac.initParametersMAC(fa, rs)
    armP = ArmParameters()
    musclesP = MusclesParameters()
    nsc = NextStateComputation()
    nsc.initParametersNSC(mac, armP, rs, musclesP)
    Ukf = UnscentedKalmanFilterControl()
    Ukf.initParametersUKF(4, 2, 25, nsc)
    cc = CostComputation()
    cc.initParametersCC(rs)
    tg = TrajectoryGenerator()
    tg.initParametersTG(armP, rs, nsc, cc, sizeOfTarget, Ukf)
    tgs = TrajectoriesGenerator()
    tgs.initParametersTGS(rs, 5, tg, 4, 6, mac)
    return tgs

def launchCMAESForSpecificTargetSize(sizeOfTarget):
    print("Start of the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    fr, rs = initFRRS()
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    theta = normalizationNP(theta, rs)
    theta = matrixToVector(theta)
    tgs = initAllUsefullObj(sizeOfTarget, fr, rs)
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, theta, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    nameToSaveThetaCma = rs.pathFolderData + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/thetaCma" + str(sizeOfTarget) + "opti1"
    np.savetxt(nameToSaveThetaCma, resCma[0])
    print("End of optimization for target " + str(sizeOfTarget) + " !")

class TrajectoriesGenerator:
    
    def __init__(self):
        self.name = "TrajectoriesGenerator"
        self.call = 0
        self.saveCost = []
        
    def initParametersTGS(self, rs, numberOfRepeat, tg, dimState, dimOutput, mac):
        self.rs = rs
        self.numberOfRepeat = numberOfRepeat
        self.tg = tg
        self.dimState = dimState
        self.dimOutput = dimOutput
        self.mac = mac
        self.posIni = np.loadtxt(self.rs.experimentFilePosIni)
    
    def runTrajectories(self):
        pass
    
    def initTheta(self, theta):
        theta = np.asarray(theta).reshape((self.rs.numfeats**self.dimState, self.dimOutput))
        self.theta = unNormNP(theta, self.rs)
        self.mac.setThetaMAC(self.theta)
    
    def runTrajectoriesCMAWithoutParallelization(self, theta):
        self.initTheta(theta)
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
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget, Ukf):
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        
    def saveDataTG(self, coordWK, coordUKF, init = 0):
        if init == 1:
            self.SaveCoordWK[self.nameToSaveTraj] = []
            self.SaveCoordUKF[self.nameToSaveTraj] = []
        self.SaveCoordWK[self.nameToSaveTraj].append(coordWK)
        self.SaveCoordUKF[self.nameToSaveTraj].append(coordUKF)
    
    def runTrajectory(self, x, y):
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = createVector(q1, q2)
        dotq = createVector(0., 0.)
        state = createStateVector(dotq, q)
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        i, t, cost = 0, 0, 0
        
        self.nameToSaveTraj = str(x) + "//" + str(y)
        self.saveDataTG(coordHand, coordHand, init = 1)
        
        while coordHand[1] <= self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                state, U = self.nsc.computeNextState(state)
                stateUKF = self.Ukf.runUKF(state)
                cost = self.cc.computeStateTransitionCost(cost, U, t)
                dotq, q = getDotQAndQFromStateVectorS(state)
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
                dotqUKF, qUKF = getDotQAndQFromStateVectorS(stateUKF)
                coordElbowUKF, coordHandUKF = mgd(qUKF, self.armP.l1, self.armP.l2)
                self.saveDataTG(coordHand, coordHandUKF)
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
        
    def initParametersMAC(self, fa, rs):
        self.fa = fa
        self.rs = rs
        
    def setThetaMAC(self, theta):
        self.theta = theta
    
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
    
    
class UnscentedKalmanFilterControl:
    
    def __init__(self):
        self.name = "UnscentedKalmanFilter"
        
    def initParametersUKF(self, dimState, dimObs, delay, nsc):
        self.dimState = dimState
        self.dimObs = dimObs
        self.delay = delay
        self.nsc = nsc
        transition_covariance = np.eye(self.dimState)*0.01
        initial_state_mean = np.zeros(self.dimState)
        observation_covariance = 1000*np.eye(self.dimObs) 
        initial_state_covariance = np.eye(self.dimState)
        self.nextCovariance = np.eye(self.dimState)*0.1
        self.ukf = UnscentedKalmanFilter(self.transitionFunctionUKF, self.observationFunctionUKF,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
    
    def transitionFunctionUKF(self, state, transitionNoise = 0):
        nextState, U = self.nsc.computeNextState(state)
        nextState = nextState.T[0]
        nextStateNoise = nextState + transitionNoise
        return nextStateNoise
    
    def observationFunctionUKF(self, state, observationNoise = 0):
        obs = np.asarray([state[2], state[3]])
        obsNoise = obs + observationNoise
        return obsNoise
    
    def initStateStore(self, state):
        self.stateStore = np.tile(state, (1, self.delay))
    
    def storeState(self, state):
        self.stateStore = np.roll(self.stateStore, 1, axis = 1)
        self.stateStore.T[0] = state.T
    
    def getObservation(self, state):
        return np.asarray([state[2, 0], state[3, 0]])
    
    def runUKF(self, state):
        self.storeState(state)
        observation = self.getObservation(state)
        nextState, self.nextCovariance = self.ukf.filter_update(self.stateStore.T[self.delay-1], self.nextCovariance, observation)
        return nextState
        
        
        