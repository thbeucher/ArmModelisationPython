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
    
    def initParamTraj(self):
        self.Usave = {}
        self.IteSave = {}
        self.lastCoord = {}
        self.saveOneTraj = {}
        self.speedSave = {}
        self.costSave = {}
    
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
    
    def initSaveData(self, name1, name2):
        '''
        Initializes object used to save data
        '''
        self.Usave[name1] = []
        if not name2 in self.speedSave:
            self.speedSave[name2] = []
        if not name2 in self.lastCoord:
            self.lastCoord[name2] = []
        if not name2 in self.IteSave:
            self.IteSave[name2] = []
    
    def saveDataB(self, name1, name2, U, coordEL, coordHA):
        '''
        Saves data which changes during the loop in generateTrajectories
        '''
        self.Usave[name1].append(U)
        self.save.SaveTrajectory(coordEL, coordHA)
    
    def saveDataf(self, name2, coordHA, i):
        '''
        Saves data generate at the end of the trajectory generation
        '''
        self.lastCoord[name2].append(coordHA)
        self.IteSave[name2].append(i)
        
    def generateTrajectories(self, xI, yI, theta, optQ = 0):
        '''
        Generates the trajectory depend of the starting point given
        
        Inputs:     -xI: scalar, absciss of the trajectory starting point
                    -yI: scalar, ordinate of the trajectory starting point
                    -Theta: Numpy array
                    
        Output:    -Ju: scalar, cost of the trajectory
        '''
        #Trick to use q1 q2 as input parameters for trajGenerator if optQ = 1
        if optQ == 1:
            q1 = xI
            q2 = yI
        elif optQ == 0:
            q1, q2 = mgi(xI, yI, self.armP.l1, self.armP.l2)
        #Initialize q and dotq
        q = np.array([[q1], [q2]])
        dotq = self.armD.get_dotq_0()
        coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
        #self.save.SaveTrajectory(coordEL, coordHA)
        t, i, Ju = 0, 0, 0#Ju = cost
        #Name used to save Data
        nameSave, nameSave2 = str(str(xI) + str(yI)), str(str(xI) + "//" + str(yI))
        #Initialization containers for saving data
        #self.initSaveData(nameSave, nameSave2)
        #compute the trajectory ie find the next point
        #as long as the target is not reach
        while coordHA[1] < (self.rs.targetOrdinate):
            #stop condition to avoid memory saturation
            if i < self.rs.numMaxIter:
                inputQ = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
                #get the muscular activation
                U = self.getCommand(inputQ, theta)
                #self.speedSave[nameSave2].append((dotq[0,0], dotq[1,0]))
                #
                ddotq, dotq, q = mdd(q, dotq, U, self.armP, self.musclesP, self.rs.dt)
                q = jointStop(q)
                coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
                #Saving data B
                #self.saveDataB(nameSave, nameSave2, U, coordEL, coordHA)
                Ju = self.costComputation(Ju, U, t)
            else:
                break
            i += 1
            t += self.rs.dt
        #print(i)
        #Saving data f
        #self.saveDataf(nameSave2, coordHA, i)
        if((coordHA[0] >= (0-self.targetSizeS/2) and coordHA[0] <= (0+self.targetSizeS/2)) and coordHA[1] >= (self.rs.targetOrdinate - self.rs.errorPosEnd)):
            Ju += self.rs.rhoCF
        self.costSave[nameSave2] = Ju
        return Ju
    


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



