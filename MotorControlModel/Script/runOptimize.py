'''
Author: Thomas Beucher

Module: runOptimize

Description: code stacker et otpimiser pour réduire le temps de calcul
'''
import sys
name = "/home/beucher/ProjetCluster/ArmModelPython/"
sys.path.append(name + "Utils")
sys.path.append(name + "ArmModel")
sys.path.append(name + "Main")
sys.path.append(name + "Regression")
sys.path.append(name + "Script")
sys.path.append(name + "Optimisation")

from Utils.ReadSetupFile import ReadSetupFile
from multiprocessing.pool import Pool
import numpy as np
from Utils.ThetaNormalization import normalization, matrixToVector,\
    vectorToMatrix, unNorm
from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters
from ArmModel.ArmDynamics import ArmDynamics, mdd
from ArmModel.GeometricModel import mgd, jointStop, mgi
from Regression.functionApproximator_RBFN import fa_rbfn
from Utils.FileReading import FileReading
from pykalman import UnscentedKalmanFilter
from Utils.FileSaving import fileSavingBin, fileSavingStr
from cma import fmin

def multiProcRO(rco):
    cost = []
    for el in rco.posIni:
        costTmp = rco.generateTrajectoriesRO(el[0], el[1])
        cost.append(costTmp)
    return cost
    

class runCmaesOpti:
    
    def __init__(self, sizeT):
        self.sizeT = sizeT/2
        self.rs = ReadSetupFile()
        self.fr = FileReading()
        self.armP = ArmParameters()
        self.musclesP = MusclesParameters()
        self.armD = ArmDynamics()
        self.posIni = self.fr.getobjread(self.rs.experimentFilePosIni)
        self.initFA()
        self.initKalmanRO()
        
    def initFA(self):
        self.fa = fa_rbfn()
        state, command = self.fr.getData(self.rs.pathFolderTrajectories)
        state, command = self.fr.dicToArray(state), self.fr.dicToArray(command)
        self.fa.setTrainingData(state.T, command.T)
        self.fa.setCentersAndWidths()
        
    def setThetaRO(self, theta):
        self.theta = theta
        
    def transition_functionRO(self, state, noise = 0):
        nextState, Utransi = self.computeNextStateRO(np.asarray([state]).T)
        nextStateNoise = nextState + np.asarray([noise]).T
        return nextStateNoise.T[0]
    
    def initKalmanRO(self):
        dimState = 4
        transition_covariance = np.eye(dimState)*0.01
        initial_state_mean = np.zeros(dimState)
        observation_covariance = 1000*np.eye(dimState)
        initial_state_covariance = np.eye(dimState)
        self.nextCovariance = np.eye(dimState)*0.1
        self.ukf = UnscentedKalmanFilter(self.transition_functionRO, self.observation_functionRO,
                                    transition_covariance, observation_covariance,
                                    initial_state_mean, initial_state_covariance)
        
    def runKalmanRO(self, state):
        self.storeStateRO(state)
        self.nextState, junk = self.ukf.filter_update(self.state_store.T[self.delay-1], self.nextCovariance, state.T[0])
        U = self.getCommandRO(np.asarray([self.nextState]).T, self.theta)
        dotq, q = self.getDotQAndQFromStateVectorRO(self.nextState)
        junk, self.coordKA = mgd(q, self.armP.l1, self.armP.l2)
        self.speedKA = np.linalg.norm(dotq)
        return U
    
    def observation_functionRO(self, inputQ, noise = 0):
        if len(inputQ.shape) == 1:
            inputQ = np.asarray([inputQ]).T
        nextState, Uobs = self.computeNextStateRO(inputQ)
        nexStateNoise = nextState + np.asarray([noise]).T
        return nexStateNoise.T[0]
    
    def storeStateRO(self, state):
        self.state_store = np.roll(self.state_store, 1, axis = 1)
        self.state_store.T[0] = state.T
        
    def getDotQAndQFromStateVectorRO(self, state):
        dotq = np.array([[state[0,0]], [state[1,0]]])
        q = np.array([[state[2,0]], [state[3,0]]])
        return dotq, q
        
    def getCommandRO(self, inputgc, theta):
        U = self.fa.computesOutput(inputgc, theta)
        UnoiseTmp = U*(1+ np.random.normal(0,self.rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    def computeNextStateRO(self, state):
        dotq, q = self.getDotQAndQFromStateVectorRO(state)
        U = self.getCommandRO(state, self.theta)
        ddotq, dotq, q = mdd(q, dotq, U, self.armP, self.musclesP, self.rs.dt)
        q = jointStop(q)
        outputQ = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
        return outputQ, U
    
    def costComputationRO(self, Ju, U, t):
        mvtCost = (np.linalg.norm(U))**2
        Ju += np.exp(-t/self.rs.gammaCF)*(-self.rs.upsCF*mvtCost)
        return Ju
        
    def generateTrajectoriesRO(self, x, y):
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
        q = np.array([[q1], [q2]])
        dotq = self.armD.get_dotq_0()
        state = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
        self.t, self.cost, i = 0, 0, 0
        coordEl, coordHa = mgd(q, self.armP.l1, self.armP.l2)
        while coordHa[1] < self.rs.targetOrdinate:
            if i < self.rs.numMaxIter:
                state, U = self.computeNextStateRO(state)
                dotq, q = self.getDotQAndQFromStateVectorRO(state)
                Uk = self.runKalmanRO(state)
                self.cost = self.costComputationRO(self.cost, Uk, self.t)
                coordEl, coordHa = mgd(q, self.armP.l1, self.armP.l2)
            else:
                break
            i += 1
            self.t += self.rs.dt
        if self.coordKA[0] >= (-self.sizeT) and self.coordKA[0] <= self.sizeT and self.coordKA[1] >= self.rs.targetOrdinate and self.speedKA < 0.5:
            self.cost += np.exp(-self.t/self.rs.gammaCF)*self.rs.rhoCF
        return self.cost
    
class LaunchCmaes:
    
    def __init__(self, rco, rs):
        self.call = 0
        self.rco = rco
        self.rs = rs
    
    def LaunchTrajCmaes(self, theta):
        theta = vectorToMatrix(theta)
        theta = unNorm(theta)
        self.rco.setThetaRO(theta)
        p = Pool(5)
        resCost = p.map(multiProcRO, [self.rco, self.rco, self.rco, self.rco, self.rco])
        meanCost = np.mean(np.asarray(resCost), axis = 0)
        costF = np.mean(meanCost)
        print("Call n°", self.call)
        self.call += 1
        print("Cost: ", costF)
        if self.call == (self.rs.maxIterCmaes * self.rs.popsizeCmaes):
            nameLT = "OptimisationResults/costEvalAll/costEval" + str(self.rco.sizeT) + str(self.call)
            fileSavingBin("")
        return costF*(-1)
        

def runCmaesRO(sizeT):
    rs = ReadSetupFile()
    print("Start process target = ", sizeT)
    theta = np.loadtxt("/home/beucher/workspace/Data/RBFN2/3feats/ThetaX7NP")
    theta = normalization(theta)
    theta = matrixToVector(theta)
    rco = runCmaesOpti(sizeT)
    ltc = LaunchCmaes(rco, rs)
    thetaCma = fmin(ltc.LaunchTrajCmaes, theta, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    print("thetaCma", thetaCma)
    nameToSaveCma = "OptimisationResults/ResCma" + str(sizeT) + "/thetaSolCma" + str(sizeT) + "try1"
    fileSavingStr(nameToSaveCma, thetaCma[0])
    fileSavingBin(nameToSaveCma + "BIN", thetaCma[0])
    
def runCmaesForMultipleTargetRO():
    rs = ReadSetupFile()
    p = Pool(4)
    p.map(runCmaesRO, rs.sizeOfTarget)
        


    
