#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True
'''
Author: Thomas Beucher

Module: testAll

Description: 
'''
import sys
name = "/home/beucher/ProjetCluster/ArmModelPython/"
sys.path.append(name + "ArmModel")
sys.path.append(name + "Utils")
sys.path.append(name + "Regression")

import cython
import time
import cma
from pykalman import UnscentedKalmanFilter
from Utils.CreateVectorUtil import createVector
from Regression.functionApproximator_RBFN import fa_rbfn
from Utils.ThetaNormalization import normalizationNP, matrixToVector, unNormNP
from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters
from Utils.InitUtil import initFRRS
import threading
import math

import numpy as np
cimport numpy as np

cdef mgi(float xi, float yi, float l1, float l2):
    cdef:
        float a
        float c
        float d
        float q1
        float q2
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
    
    
cdef mgd(object[np.double_t, ndim = 2] q, float l1, float l2):
    cdef:
        tuple coordElbow
        tuple coordHand
    coordElbow = (l1*np.cos(q[0,0]), l1*np.sin(q[0,0]))
    coordHand = (l2*np.cos(q[1,0] + q[0,0]) + l1*np.cos(q[0,0]), l2*np.sin(q[1,0] + q[0,0]) + l1*np.sin(q[0,0]))
    return coordElbow, coordHand
    
    
cdef np.ndarray jointStop(object[np.double_t, ndim = 2] q):
    if q[0,0] < -0.6:
        q[0,0] = -0.6
    elif q[0,0] > 2.6:
        q[0,0] = 2.6
    if q[1,0] < -0.2:
        q[1,0] = -0.2
    elif q[1,0] > 3.0:
        q[1,0] = 3.0
    return q

cdef np.ndarray createStateVector(object[np.double_t, ndim = 2] dotq, object[np.double_t, ndim = 2] q):
    cdef np.ndarray[np.double_t, ndim = 2] inputQ
    inputQ = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
    return inputQ
    
cdef getDotQAndQFromStateVectorS(object[np.double_t, ndim = 2] inputQ):
    cdef:
        np.ndarray[np.double_t, ndim = 2] dotq
        np.ndarray[np.double_t, ndim = 2] q
    dotq = np.array([[inputQ[0,0]], [inputQ[1,0]]])
    q = np.array([[inputQ[2,0]], [inputQ[3,0]]])
    return dotq, q


cdef object initController(object rs, object fr):
    cdef object fa
    fa = fa_rbfn(rs.numfeats)
    state, command = fr.getData(rs.pathFolderTrajectories)
    stateAll, commandAll = fr.dicToArray(state), fr.dicToArray(command)
    fa.setTrainingData(stateAll.T, commandAll.T)
    fa.setCentersAndWidths()
    return fa

cpdef object initAllUsefullObj(sizeOfTarget, object fr, object rs):
    cdef:
        object fa
        object mac
        object armP
        object musclesP
        object armD
        object nsc
        object Ukf
        object cc
        object tg
        object tgs
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

cdef void launchCMAESForSpecificTargetSize(sizeOfTarget):
    cdef:
        object fr
        object rs
        np.ndarray theta
        object tgs
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

def launchCMAESForAllTargetSize():
    print("launch")
    fr, rs = initFRRS()
    for i in range(len(rs.sizeOfTarget)):
        launchCMAESForSpecificTargetSize(rs.sizeOfTarget[i])

cdef class ArmDynamics:
    cdef:
        np.ndarray dotq0
        np.ndarray state
        object armP
        object musclesP
        float dt
    
    def __init__(self):
        self.dotq0 = np.array([[0.],[0.]])
        
    cpdef initStateAD(self, object[np.double_t, ndim = 2] state):
        self.state = state
        
    cpdef initParametersAD(self, object armP, object musclesP, float dt):
        self.armP = armP
        self.musclesP = musclesP
        self.dt = dt
        
    cpdef setNewStateAD(self, object[np.double_t, ndim = 2] dotq, object[np.double_t, ndim = 2] q):
        self.state = createStateVector(dotq, q)
        
    cpdef np.ndarray mddAD(self, object[np.double_t, ndim = 2] U):
        cdef:
            np.ndarray[np.double_t, ndim = 2] dotq
            np.ndarray[np.double_t, ndim = 2] q
            np.ndarray[np.double_t, ndim = 2] M
            np.ndarray[np.double_t, ndim = 2] C
            np.ndarray[np.double_t, ndim = 2] Minv
            np.ndarray[np.double_t, ndim = 2] Q
            np.ndarray[np.double_t, ndim = 2] Gamma
            np.ndarray[np.double_t, ndim = 2] ddotq
        M = np.array([[self.armP.k1+2*self.armP.k2*math.cos(self.state[3,0]),self.armP.k3+self.armP.k2*math.cos(self.state[3,0])],[self.armP.k3+self.armP.k2*math.cos(self.state[3,0]),self.armP.k3]])
        C = np.array([[-self.state[1,0]*(2*self.state[0,0]+self.state[1,0])*self.armP.k2*math.sin(self.state[3,0])],[(self.state[0,0]**2)*self.armP.k2*math.sin(self.state[3,0])]])
        Minv = np.linalg.inv(M)
        Q = np.diag([self.state[2,0], self.state[2,0], self.state[3,0], self.state[3,0], self.state[2,0], self.state[2,0]])
        Gamma = np.dot((np.dot(self.armP.At, self.musclesP.fmax)-np.dot(self.musclesP.Knulle, Q)), U)
        dotq, q = getDotQAndQFromStateVectorS(self.state)
        ddotq = np.dot(Minv,(Gamma - C - np.dot(self.armP.B, dotq)))
        dotq += ddotq*self.dt
        q += dotq*self.dt
        self.setNewStateAD(dotq, q)
        return self.state
    
    cpdef np.ndarray mddADUKF(self, object[np.double_t, ndim = 2] U, object[np.double_t, ndim = 2] state):
        cdef:
            np.ndarray[np.double_t, ndim = 2] dotq
            np.ndarray[np.double_t, ndim = 2] q
            np.ndarray[np.double_t, ndim = 2] M
            np.ndarray[np.double_t, ndim = 2] C
            np.ndarray[np.double_t, ndim = 2] Minv
            np.ndarray[np.double_t, ndim = 2] Q
            np.ndarray[np.double_t, ndim = 2] Gamma
            np.ndarray[np.double_t, ndim = 2] ddotq
        dotq, q = getDotQAndQFromStateVectorS(state)
        M = np.array([[self.armP.k1+2*self.armP.k2*math.cos(q[1,0]),self.armP.k3+self.armP.k2*math.cos(q[1,0])],[self.armP.k3+self.armP.k2*math.cos(q[1,0]),self.armP.k3]])
        C = np.array([[-dotq[1,0]*(2*dotq[0,0]+dotq[1,0])*self.armP.k2*math.sin(q[1,0])],[(dotq[0,0]**2)*self.armP.k2*math.sin(q[1,0])]])
        Minv = np.linalg.inv(M)
        Q = np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])
        Gamma = np.dot((np.dot(self.armP.At, self.musclesP.fmax)-np.dot(self.musclesP.Knulle, Q)), U)
        ddotq = np.dot(Minv,(Gamma - C - np.dot(self.armP.B, dotq)))
        dotq += ddotq*self.dt
        q += dotq*self.dt
        nextState = createStateVector(dotq, q)
        return nextState
    
cdef mdd(object[np.double_t, ndim = 2] q, object[np.double_t, ndim = 2] dotq, object[np.double_t, ndim = 2] U, object armP, object musclesP, float dt):
    cdef:
        np.ndarray[np.double_t, ndim = 2] M
        np.ndarray[np.double_t, ndim = 2] C
        np.ndarray[np.double_t, ndim = 2] Minv
        np.ndarray[np.double_t, ndim = 2] Q
        np.ndarray[np.double_t, ndim = 2] Gamma
        np.ndarray[np.double_t, ndim = 2] ddotq
    M = np.array([[armP.k1+2*armP.k2*math.cos(q[1,0]),armP.k3+armP.k2*math.cos(q[1,0])],[armP.k3+armP.k2*math.cos(q[1,0]),armP.k3]])
    C = np.array([[-dotq[1,0]*(2*dotq[0,0]+dotq[1,0])*armP.k2*math.sin(q[1,0])],[(dotq[0,0]**2)*armP.k2*math.sin(q[1,0])]])
    Minv = np.linalg.inv(M)
    Q = np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])
    Gamma = np.dot((np.dot(armP.At, musclesP.fmax)-np.dot(musclesP.Knulle, Q)), U)
    ddotq = np.dot(Minv,(Gamma - C - np.dot(armP.B, dotq)))
    dotq += ddotq*dt
    q += dotq*dt
    return ddotq, dotq, q

class myThread(threading.Thread):
    def __init__(self, tg, posIni):
        threading.Thread.__init__(self)
        self.tg = tg
        self.posIni = posIni
        self.ret = None
    def run(self):
        self.ret = [self.tg.runTrajectory(xy[0], xy[1]) for xy in self.posIni]
    def join(self):
        threading.Thread.join(self)
        return self.ret

cdef class TrajectoriesGenerator:
    cdef:
        int call
        list saveCost
        object rs
        object tg
        object mac
        int numberOfRepeat
        int dimState
        int dimOutput
        np.ndarray theta
        np.ndarray posIni
    
    def __init__(self):
        self.call = 0
        self.saveCost = []
        
    cpdef initParametersTGS(self, object rs, int numberOfRepeat, object tg, int dimState, int dimOutput, object mac):
        self.rs = rs
        self.numberOfRepeat = numberOfRepeat
        self.tg = tg
        self.dimState = dimState
        self.dimOutput = dimOutput
        self.mac = mac
        self.posIni = np.loadtxt(self.rs.pathFolderData + self.rs.experimentFilePosIni)
    
    cpdef initTheta(self, object theta):
        theta = np.asarray(theta).reshape((self.rs.numfeats**self.dimState, self.dimOutput))
        self.theta = unNormNP(theta, self.rs)
        self.mac.setThetaMAC(self.theta)
    
    cpdef float runTrajectoriesCMAWithoutParallelization(self, object theta):
        cdef:
            np.ndarray meanByTraj
            float meanAll
        t0 = time.time()
        self.initTheta(theta)
        costAll = [[self.tg.runTrajectory(xy[0], xy[1]) for xy in self.posIni] for i in range(self.numberOfRepeat)]
        #thr = [myThread(self.tg, self.posIni) for i in range(self.numberOfRepeat)]
        #[el.start() for el in thr]
        #costAll = [el.join() for el in thr]
        meanByTraj = np.mean(np.asarray(costAll).reshape((self.numberOfRepeat, self.posIni.shape[0])), axis = 0)    
        meanAll = np.mean(meanByTraj)
        self.saveCost.append(meanAll)
        print("Call n°: ", self.call, "\nCost: ", meanAll, "\nTime: ", time.time() - t0)
        self.call += 1
        return meanAll*(-1)
    

cdef class TrajectoryGenerator:
    cdef:
        object armP
        object rs
        object nsc
        object cc
        object Ukf
        object armD
        object mac
        float sizeOfTarget
        
    cpdef initParametersTG(self, object armP, object rs, object nsc, object cc, sizeOfTarget, object Ukf, object armD, object mac):
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        self.mac = mac
    
    cpdef float runTrajectory(self, float x, float y):
        cdef:
            float q1
            float q2
            np.ndarray q
            np.ndarray dotq
            np.ndarray state
            tuple coordElbow
            tuple coordHand
            int i = 0
            float t = 0
            float cost = 0
            np.ndarray Ucontrol
            np.ndarray realState
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = createVector(q1, q2)
        dotq = createVector(0., 0.)
        state = createStateVector(dotq, q)
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
        #i, t, cost = 0, 0, 0
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
            
cdef class CostComputation:
    cdef:
        object rs
        
    cpdef initParametersCC(self, object rs):
        self.rs = rs
        
    cpdef float computeStateTransitionCost(self, float cost, np.ndarray U, float t):
        cdef float mvtCost
        mvtCost = (np.linalg.norm(U))**2
        cost += np.exp(-t/self.rs.gammaCF)*(-self.rs.upsCF*mvtCost)
        return cost
    
    cpdef float computeFinalCostReward(self, float cost, float t):
        cost += np.exp(-t/self.rs.gammaCF)*self.rs.rhoCF
        return cost

cdef class NextStateComputation:
    cdef:
        object mac
        object armP
        object rs
        object musclesP
        
    cpdef initParametersNSC(self, object mac, object armP, object rs, object musclesP):
        self.mac = mac
        self.armP = armP
        self.rs = rs
        self.musclesP = musclesP
    
cdef class MuscularActivationCommand:
    cdef:
        object fa
        object rs
        np.ndarray theta
        
    cpdef initParametersMAC(self, object fa, object rs):
        self.fa = fa
        self.rs = rs
        
    cpdef setThetaMAC(self, np.ndarray theta):
        self.theta = theta
    
    cpdef object getCommandMAC(self, np.ndarray state):
        cdef:
            np.ndarray U
            np.ndarray UnoiseTmp
            np.ndarray Unoise
        U = self.fa.computesOutput(state, self.theta)
        UnoiseTmp = U*(1+ np.random.normal(0,self.rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    
cdef class UnscentedKalmanFilterControl:
    cdef:
        int dimState
        int dimObs
        int delay
        object nsc
        object armD
        object mac
        np.ndarray nextCovariance
        object ukf
        np.ndarray obsStore

        
    cpdef initParametersUKF(self, int dimState, int dimObs, int delay, object nsc, object armD, object mac):
        cdef:
            np.ndarray transition_covariance
            np.ndarray initial_state_mean
            np.ndarray observation_covariance
            np.ndarray initial_state_covariance
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
        self.nextCovariance = np.eye(self.dimState)*0.01
        self.ukf = UnscentedKalmanFilter(self.transitionFunctionUKF, self.observationFunctionUKF,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
    
    cpdef setDelayUKF(self, int delay):
        self.delay = delay
    
    cpdef object transitionFunctionUKF(self, object stateU, object transitionNoise):
        cdef:
            np.ndarray nextX
            np.ndarray nextStateU
            np.ndarray nextStateUNoise
        nextX = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        nextStateU = self.mac.getCommandMAC(nextX)
        nextStateUNoise = nextStateU.T[0] + transitionNoise
        return nextStateUNoise
    
    cpdef object observationFunctionUKF(self, object stateU, object observationNoise):
        cdef:
            np.ndarray nextObs
            np.ndarray nextObsNoise
        nextObs = self.armD.mddADUKF(np.asarray(stateU).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        nextObsNoise = nextObs.T[0] + observationNoise
        return nextObsNoise
    
    cpdef initObsStore(self, np.ndarray state):
        self.obsStore = np.tile(state, (1, self.delay))
    
    cpdef storeObs(self, np.ndarray state):
        self.obsStore = np.roll(self.obsStore, 1, axis = 1)
        self.obsStore.T[0] = state.T
    
    cpdef object runUKF(self, np.ndarray stateU, np.ndarray obs):
        cdef:
            object nextState
            object nextCovariance
            np.ndarray stateApprox
        self.storeObs(obs)
        nextState, nextCovariance = self.ukf.filter_update(stateU.T[0], self.nextCovariance, self.obsStore.T[self.delay-1])
        stateApprox = self.armD.mddADUKF(np.asarray(nextState).reshape((self.dimState, 1)), np.asarray(self.obsStore.T[self.delay-1]).reshape((self.dimObs, 1)))
        return stateApprox
        
        
        
