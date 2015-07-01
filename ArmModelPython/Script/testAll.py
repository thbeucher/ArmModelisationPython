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
from ArmModel.ArmDynamics import mdd, ArmDynamics
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
    armD = ArmDynamics()
    armD.initParametersAD(armP, musclesP, rs.dt)
    nsc = NextStateComputation()
    nsc.initParametersNSC(mac, armP, rs, musclesP)
    Ukf = UnscentedKalmanFilterControl()
    Ukf.initParametersUKF(6, 4, 25, nsc, armD, mac)
    cc = CostComputation()
    cc.initParametersCC(rs)
    tg = TrajectoryGenerator()
    tg.initParametersTG(armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac)
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
        self.posIni = np.loadtxt(self.rs.pathFolderData + self.rs.experimentFilePosIni)
    
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
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac):
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        self.mac = mac
        
    def saveDataTG(self, coordUKF, coordVerif, init = 0):
        if init == 1:
            self.SaveCoordUKF, self.SaveCoordVerif = {}, {}
            self.SaveCoordUKF[self.nameToSaveTraj] = []
            self.SaveCoordVerif[self.nameToSaveTraj] = []
        self.SaveCoordUKF[self.nameToSaveTraj].append(coordUKF)
        self.SaveCoordVerif[self.nameToSaveTraj].append(coordVerif)
    
    def runTrajectory(self, x, y):
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = createVector(q1, q2)
        dotq = createVector(0., 0.)
        state = createStateVector(dotq, q)
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        i, t, cost = 0, 0, 0
        self.Ukf.initObsStore(state)
        self.armD.initStateAD(state)
        while coordHand[1] < self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                Ucontrol = self.mac.getCommandMAC(state)
                realState = self.armD.mddAD(Ucontrol)
                state = self.Ukf.runUKF(Ucontrol, realState)
                cost = self.cc.computeStateTransitionCost(cost, Ucontrol, t)
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
        cost += np.exp(-t/self.rs.gammaCF)*self.rs.rhoCF
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
        
    def initParametersUKF(self, dimState, dimObs, delay, nsc, armD, mac):
        self.dimState = dimState
        self.dimObs = dimObs
        self.delay = delay
        self.nsc = nsc
        self.armD = armD
        self.mac = mac
        transition_covariance = np.eye(self.dimState)*0.01
        initial_state_mean = np.zeros(self.dimState)
        observation_covariance = 1000*np.eye(self.dimObs) 
        initial_state_covariance = np.eye(self.dimState)
        self.nextCovariance = np.eye(self.dimState)*0.0001
        self.ukf = UnscentedKalmanFilter(self.transitionFunctionUKF, self.observationFunctionUKF,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
    
    def setDelayUKF(self, delay):
        self.delay = delay
    
    def transitionFunctionUKF(self, stateU, transitionNoise = 0):
        nextX = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        nextStateU = self.mac.getCommandMAC(nextX)
        nextStateUNoise = nextStateU.T[0] + transitionNoise
        return nextStateUNoise
    
    def observationFunctionUKF(self, stateU, observationNoise = 0):
        nextObs = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        nextObsNoise = nextObs.T[0] + observationNoise
        return nextObsNoise
    
    def initObsStore(self, state):
        self.obsStore = np.tile(state, (1, self.delay))
    
    def storeObs(self, state):
        self.obsStore = np.roll(self.obsStore, 1, axis = 1)
        self.obsStore.T[0] = state.T
    
    def runUKF(self, stateU, obs):
        self.storeObs(obs)
        nextState, nextCovariance = self.ukf.filter_update(stateU.T[0], self.nextCovariance, self.obsStore.T[self.delay-1])
        stateApprox = self.armD.mddADUKF(np.asarray(nextState).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        return stateApprox
        
        
        