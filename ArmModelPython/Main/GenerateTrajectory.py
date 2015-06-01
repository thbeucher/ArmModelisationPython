'''
Author: Thomas Beucher

Module: GenerateTrajectory

Description: This class is used to generate trajectory.
                During the generation, the cost is compute
'''
from Utils.FileReading import FileReading
from Utils.ReadSetupFile import ReadSetupFile
from Regression.functionApproximator_RBFN import fa_rbfn
import numpy as np
from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters
from ArmModel.ArmDynamics import ArmDynamics, mdd
from ArmModel.GeometricModel import mgi, mgd, jointStop
from ArmModel.SavingData import SavingData
from Utils.GenerateTrajectoryUtils import kalmanFilterInit,\
    getDotQAndQFromStateVectorS, createStateVector


class GenerateTrajectory:
    
    def __init__(self, nbtarget = 0, targetSize = 0):
        '''
        class parameters initialization
        '''
        self.super = "SuperInit"
        if nbtarget == 0:
            self.targetSizeS = 0.1
        elif nbtarget == 4:
            self.targetSizeS = targetSize
        self.save = SavingData()
        self.armP = ArmParameters()
        self.musclesP = MusclesParameters()
        self.armD = ArmDynamics()
        self.fr = FileReading()
        self.rs = ReadSetupFile()
        #Initialisation des outils permettant d'utiliser le controleur rbfn
        self.fa = fa_rbfn(self.rs.numfeats)
        state, command = self.fr.getData(self.rs.pathFolderTrajectories)
        stateAll, commandAll = self.fr.dicToArray(state), self.fr.dicToArray(command)
        self.fa.setTrainingData(stateAll.T, commandAll.T)
        self.fa.setCentersAndWidths()
        #Recuperation des positions initiales de l'experimentation
        self.posIni = self.fr.getobjread(self.rs.experimentFilePosIni)
        #Object used to save data
        self.initParamTraj()
        self.delay = 3
    
    def initParamTraj(self):
        self.Usave = {}
        self.IteSave = {}
        self.lastCoord = {}
        self.saveOneTraj = {}
        self.speedSave = {}
        self.costSave = {}
        self.actiMuscuSave = {}
        self.stateAndCommand = {}
        self.coordEndEffector = {}
    
    def costComputation(self, Ju, U, t):
        '''
        Computes the cost for the muscular activation vector given
            
        Inputs:     -Ju: scalar, trajectory cost at the time t
                    -U: (6,1) numpy array, muscular activation vector
                    -t: scalar, the time
        
        Outputs:    -Ju: scalar, cost
        '''
        mvtCost = (np.linalg.norm(U))**2
        Ju += np.exp(-t/self.rs.gammaCF)*(-self.rs.upsCF*mvtCost)
        return Ju
        
        
    def getCommand(self, inputgc, theta):
        '''
        Returns the muscular activation vector U from the position vector Q
        Inputs:     -inputgc: (4,1) numpy array, vector [dotq1, dotq2, q1, q2]
                    -theta: 2D numpy array, the controler generate by rbfn
        
        Outputs:    -Unoise: (6,1) numpy array, noisy muscular activation vector
        '''
        U = self.fa.computesOutput(inputgc, theta)
        #Noise for muscular activation
        UnoiseTmp = U*(1+ np.random.normal(0,self.rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
    
    def initSaveData(self):
        '''
        Initializes object used to save data
        '''
        self.Usave[self.name1] = []
        if not self.name2 in self.speedSave:
            self.speedSave[self.name2] = []
        if not self.name2 in self.lastCoord:
            self.lastCoord[self.name2] = []
        if not self.name2 in self.IteSave:
            self.IteSave[self.name2] = []
        if not self.name2 in self.actiMuscuSave:
            self.actiMuscuSave[self.name2] = []
        if not self.name2 in self.stateAndCommand:
            self.stateAndCommand[self.name2] = []
        if not self.name2 in self.coordEndEffector:
            self.coordEndEffector[self.name2] = []
    
    def saveDataB(self, coordEL, coordHA, inputQ, dotq, U):
        '''
        Saves data which changes during the loop in generateTrajectories
        '''
        self.Usave[self.name1].append(U)
        self.save.SaveTrajectory(coordEL, coordHA)
        self.stateAndCommand[self.name2].append((inputQ, U))
        self.coordEndEffector[self.name2].append(coordHA)
        self.speedSave[self.name2].append((dotq[0,0], dotq[1,0]))
    
    def saveDataf(self, coordHA, i, Ju):
        '''
        Saves data generate at the end of the trajectory generation
        '''
        self.lastCoord[self.name2].append(coordHA)
        self.IteSave[self.name2].append(i)
        self.actiMuscuSave[self.name2].append(Ju)
        
    def transition_function(self, state, noise = 0):
        '''
        transition_functions[t] is a function of the state and the transition noise at time t 
        and produces the state at time t+1
        
        Input:     -inputQ: numpy array (state_dimension, ), the state vector s at time t (dotq1, dotq2, q1, q2)
        
        Output:    -outputQ: numpy array (state_dimension, ), the state vector at time t+1
        '''
        nextState, Utransi = self.computeNextState(state)
        nextStateNoise = nextState + noise
        return nextStateNoise
    
    def computeNextState(self, inputQ):
        '''
        Computes the next state
        
        Input:     -inputQ: numpy array (state_dimension, ), the state vector s at time t (dotq1, dotq2, q1, q2)
        
        Output:    -outputQ: numpy array (state_dimension, ), the state vector at time t+1
        '''
        dotq, q = getDotQAndQFromStateVectorS(inputQ)
        U = self.getCommand(inputQ, self.theta)
        ddotq, dotq, q = mdd(q, dotq, self.U, self.armP, self.musclesP, self.rs.dt)
        q = jointStop(q)
        outputQ = createStateVector(dotq, q)
        return outputQ, U
    
    def observation_function(self, inputQ, noise = 0):
        '''
        observation_functions[t] is a function of the state and the observation noise at time t 
        and produces the observation at time t
        '''
        state = inputQ[0]
        nextState, Uobs = self.computeNextState(state)
        nexStateNoise = nextState + noise
        return nexStateNoise    
    
    def storeState(self, state):
        self.obs_store = np.roll(self.obs_store, 1, axis = 0)
        self.obs_store[0] = state
        
    def generateTrajectories(self, xI, yI, theta, optQ = 0):
        '''
        Generates the trajectory depend of the starting point given
        
        Inputs:     -xI: scalar, absciss of the trajectory starting point
                    -yI: scalar, ordinate of the trajectory starting point
                    -Theta: Numpy array
                    
        Output:    -Ju: scalar, cost of the trajectory
        '''
        self.theta = theta
        #Trick to use q1 q2 as input parameters for trajGenerator if optQ = 1
        if optQ == 1:
            q1, q2 = xI, yI
        elif optQ == 0:
            q1, q2 = mgi(xI, yI, self.armP.l1, self.armP.l2)
        #Initialize q and dotq
        q = np.array([[q1], [q2]])
        dotq = self.armD.get_dotq_0()
        inputQ = createStateVector(dotq, q)
        coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
        self.save.SaveTrajectory(coordEL, coordHA)
        self.t, i, self.Ju = 0, 0, 0#Ju = cost
        #Name used to save Data
        self.name1, self.name2 = str(str(xI) + str(yI)), str(str(xI) + "//" + str(yI))
        #Initialization containers for saving data
        self.initSaveData()
        #Kalman filter init
        ukf, nextCovariance = kalmanFilterInit()
        self.obs_store = np.tile(inputQ, (self.delay, 1))
        #compute the trajectory ie find the next point
        #as long as the target is not reach
        while coordHA[1] < (self.rs.targetOrdinate):
            #stop condition to avoid memory saturation
            if i < self.rs.numMaxIter:
                inputQ, U = self.computeNextState(inputQ)
                dotq, q = getDotQAndQFromStateVectorS(inputQ)
                #Kalman filter
                self.storeState(inputQ)
                observation = self.observation_function(self.obs_store[self.delay-1])
                nextState, nextCovariance = ukf.filter_update(inputQ, nextCovariance, observation)
                #saving data
                coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
                self.saveDataB(coordEL, coordHA, inputQ, dotq, U)
                #compute cost
                self.Ju = self.costComputation(self.Ju, U, self.t)
            else:
                break
            i += 1
            self.t += self.rs.dt
        #print(i)
        #Saving data f
        self.saveDataf(coordHA, i, self.Ju)
        if((coordHA[0] >= (0-self.targetSizeS/2) and coordHA[0] <= (0+self.targetSizeS/2)) and coordHA[1] >= (self.rs.targetOrdinate - self.rs.errorPosEnd)):
            self.Ju += np.exp(-self.t/self.rs.gammaCF)*self.rs.rhoCF
        self.costSave[self.name2] = self.Ju
        return self.Ju
    


    def generateTrajectoriesWithU(self, U, save):
        '''
        compute the trajectory using U as input.
        Actually not used
        '''
        q = np.array([[np.pi/2], [0]])
        dotq = self.armD.dotq0
        coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
        save.SaveTrajectory(coordEL, coordHA)
        t = 0
        while t <= 1:
            ddotq, dotq, q = mdd(q, dotq, U, self.armP, self.musclesP, self.rs.dt)
            coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
            save.SaveTrajectory(coordEL, coordHA)
            q = jointStop(q)
            t += self.rs.dt



