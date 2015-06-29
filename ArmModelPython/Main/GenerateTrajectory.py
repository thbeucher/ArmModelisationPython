'''
Author: Thomas Beucher

Module: GenerateTrajectory

Description: This class is used to generate trajectory.
                During the generation, the cost is compute
'''
from Regression.functionApproximator_RBFN import fa_rbfn
import numpy as np
from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters
from ArmModel.ArmDynamics import ArmDynamics, mdd
from ArmModel.GeometricModel import mgi, mgd, jointStop
from ArmModel.SavingData import SavingData
from Utils.GenerateTrajectoryUtils import getDotQAndQFromStateVectorS, createStateVector,\
    NextState
from Utils.InitUtil import initFRRS
from Script.KalmanModule import KalmanModule
import time

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
        self.fr, self.rs = initFRRS()
        #Initialisation des outils permettant d'utiliser le controleur rbfn
        self.fa = fa_rbfn(self.rs.numfeats)
        state, command = self.fr.getData(self.rs.pathFolderTrajectories)
        stateAll, commandAll = self.fr.dicToArray(state), self.fr.dicToArray(command)
        self.fa.setTrainingData(stateAll.T, commandAll.T)
        self.fa.setCentersAndWidths()
        #Recuperation des positions initiales de l'experimentation
        #self.posIni = self.fr.getobjread(self.rs.experimentFilePosIni)
        self.posIni = np.loadtxt(self.rs.pathFolderData + self.rs.experimentFilePosIni)
        #Object used to save data
        self.initParamTraj()
        
    
    def initParamTraj(self):
        self.Usave = {}
        self.IteSave = {}
        self.lastCoord = {}
        self.lastCoordKM = {}
        self.saveOneTraj = {}
        self.speedSave = {}
        self.speedSaveKM = {}
        self.costSave = {}
        self.actiMuscuSave = {}
        self.actiMuscuSaveKM = {}
        self.stateAndCommand = {}
        self.coordEndEffector = {}
        
    def setTheta(self, theta, dt = 0):
        self.theta = theta
        if dt == 0:
            self.NS = NextState(self.armP, self.musclesP, self.rs.dt, self.theta, self.fa, self.rs.knoiseU)
        else:
            self.NS = NextState(self.armP, self.musclesP, dt, self.theta, self.fa, self.rs.knoiseU)
    
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
    
    def initSaveData(self):
        '''
        Initializes object used to save data
        '''
        self.Usave[self.name1] = []
        if not self.name2 in self.speedSave:
            self.speedSave[self.name2] = []
        if not self.name2 in self.speedSaveKM:
            self.speedSaveKM[self.name2] = []
        if not self.name2 in self.lastCoord:
            self.lastCoord[self.name2] = []
        if not self.name2 in self.lastCoordKM:
            self.lastCoordKM[self.name2] = []
        if not self.name2 in self.IteSave:
            self.IteSave[self.name2] = []
        if not self.name2 in self.actiMuscuSave:
            self.actiMuscuSave[self.name2] = []
        if not self.name2 in self.actiMuscuSaveKM:
            self.actiMuscuSaveKM[self.name2] = []
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
        self.speedSave[self.name2].append((dotq[0,0], dotq[1,0], np.linalg.norm(dotq)))
    
    def saveDataf(self, coordHA, i, Ju, JuK, coordHAKM):
        '''
        Saves data generate at the end of the trajectory generation
        '''
        self.lastCoord[self.name2].append(coordHA)
        self.lastCoordKM[self.name2].append(coordHAKM)
        self.IteSave[self.name2].append(i)
        self.actiMuscuSave[self.name2].append(Ju)
        self.actiMuscuSaveKM[self.name2].append(JuK)
        #self.speedSaveKM[self.name2] = self.KM.saveSpeed[self.name2]
        
    def generateTrajectories(self, xI, yI, optQ = 0):
        '''
        Generates the trajectory depend of the starting point given
        
        Inputs:     -xI: scalar, absciss of the trajectory starting point
                    -yI: scalar, ordinate of the trajectory starting point
                    -Theta: Numpy array
                    
        Output:    -Ju: scalar, cost of the trajectory
        '''
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
        self.t, i, self.Ju, self.JuK = 0, 0, 0, 0#Ju = cost
        #Name used to save Data
        self.name1, self.name2 = str(str(xI) + str(yI)), str(str(xI) + "//" + str(yI))
        #Initialization containers for saving data
        self.initSaveData()
        #KalmanModule
        #self.KM = KalmanModule(self.NS, inputQ, self.name2, self.armP, self.rs)
        #compute the trajectory ie find the next point
        #as long as the target is not reach
        while coordHA[1] < (self.rs.targetOrdinate):
            #stop condition to avoid memory saturation
            if i < self.rs.numMaxIter:
                inputQ, U = self.NS.computeNextState(inputQ)
                dotq, q = getDotQAndQFromStateVectorS(inputQ)
                #run Kalman
                #Uk = self.KM.runKalman(inputQ, i)
                #self.JuK = self.costComputation(self.JuK, Uk, self.t)
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
        #Kalman
        #self.JuK, coordHAKM = self.KM.endRoutine(inputQ, self.t, self.JuK, self.costComputation)
        coordHAKM = 0
        self.saveDataf(coordHA, i, self.Ju, self.JuK, coordHAKM)
        '''for key, val in self.KM.saveAllCoord.items():
            #print(len(val), val[len(val)-1][0], "\n", val[len(val)-1][1], "\n", coordHA[0], "\n", coordHA[1])
            #if((val[len(val)-1][0] >= (0-self.targetSizeS/2) and val[len(val)-1][0] <= (0+self.targetSizeS/2)) and val[len(val)-1][1] >= (self.rs.targetOrdinate - self.rs.errorPosEnd)) and self.KM.saveSpeed[self.name2][i-1] < 0.5:
            if((val[len(val)-1][0] >= (0-self.targetSizeS/2) and val[len(val)-1][0] <= (0+self.targetSizeS/2)) and val[len(val)-1][1] >= (self.rs.targetOrdinate - self.rs.errorPosEnd)):
                self.JuK += np.exp(-self.t/self.rs.gammaCF)*self.rs.rhoCF
        return self.JuK'''
        #if((coordHA[0] >= (0-self.targetSizeS/2) and coordHA[0] <= (0+self.targetSizeS/2)) and coordHA[1] >= (self.rs.targetOrdinate - self.rs.errorPosEnd)):
        #Condition to obtain the reward for cmaes optimization
        if((coordHA[0] >= (0-self.targetSizeS/2) and coordHA[0] <= (0+self.targetSizeS/2)) and coordHA[1] >= (self.rs.targetOrdinate - self.rs.errorPosEnd)) and self.speedSave[self.name2][i-1][2] < 1:
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



