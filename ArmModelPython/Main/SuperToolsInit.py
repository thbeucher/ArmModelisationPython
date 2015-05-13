'''
Author: Thomas Beucher

Module: SuperToolsInit

Description: On retrouve dans ce fichier une classe initialisant toutes les classes utiles au projet
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
import matplotlib.pyplot as plt
from matplotlib import animation


class SuperToolsInit:
#Thomas: renommer cette classe (Main?)
    
    def __init__(self, nbtarget = 0, targetSize = 0):
        '''
        class parameters initialization
        '''
        self.super = "SuperInit"
        self.nbTarget = nbtarget
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
    
    def costFunction(self, Ju, U, t):
#Thomas: renommer : getCostFunction
#Thomas: pourquoi ça n'est pas dans Optimisation/costFunction.py?
        '''
        Computes the cost of the trajectory
            
        Inputs:     -Ju: scalar, trajectory cost at the time t
                    -U: (6,1) numpy array, muscular activation vector
                    -t: scalar, the time
        
        Outputs:    -Ju: scalar, cost
        '''
        mvtCost = (np.linalg.norm(U))**2
        Ju += np.exp(-t/self.rs.gammaCF)*(-self.rs.upsCF*mvtCost)
        return Ju
        
        
    def getCommand(self, inputgc, theta):
            #Thomas: dire ce que contiennent inputgc et theta: c'est quoi ?
        '''
        Returns the muscular activation vector U from the position vector Q
        Inputs:     -inputgc: (4,1) numpy array
                    -theta: 2D numpy array
        
        Outputs:    -Unoise: (6,1) numpy array, noisy muscular activation vector
        '''
        U = self.fa.functionApproximatorOutput(inputgc, theta)
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
        self.Usave[name1] = []
        if not name2 in self.speedSave:
            self.speedSave[name2] = []
        if not name2 in self.lastCoord:
            self.lastCoord[name2] = []
        if not name2 in self.IteSave:
            self.IteSave[name2] = []
    
    def saveDataB(self, name1, name2, U, coordEL, coordHA):
        self.Usave[name1].append(U)
        self.save.SaveTrajectory(coordEL, coordHA)
    
    def saveDataf(self, name2, coordHA, i):
        self.lastCoord[name2].append(coordHA)
        self.IteSave[name2].append(i)
        
    def trajGenerator(self, xI, yI, theta, optQ = 0):
#Thomas: renommer (generateTrajectories?)
#Thomas: cette méthode est trop longue, la décomposer/simplifier
#Thomas: cette méthode devrait être ailleurs, dans une classe qui définit le setUp
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
        q = np.array([[q1], [q2]])
        dotq = self.armD.get_dotq_0()
        coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
        self.save.SaveTrajectory(coordEL, coordHA)
        t, i, Ju = 0, 0, 0#Ju = cost
        #Name used to save Data
        nameSave = str(str(xI) + str(yI))
        nameSave2 = str(str(xI) + "//" + str(yI))
        #Initialization containers for saving data
        #self.initSaveData(nameSave, nameSave2)
        
        while coordHA[1] < (self.rs.targetOrdinate - self.rs.errorPosEnd):
            if i < self.rs.numMaxIter:
                inputQ = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
                U = self.getCommand(inputQ, theta)
                #self.speedSave[nameSave2].append((dotq[0,0], dotq[1,0]))
                ddotq, dotq, q = mdd(q, dotq, U, self.armP, self.musclesP, self.rs.dt)
                q = jointStop(q)
                coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
                #Saving data B
                #self.saveDataB(nameSave, nameSave2, U, coordEL, coordHA)
                Ju = self.costFunction(Ju, U, t)
            else:
                break
            i += 1
            t += self.rs.dt
        #print(i)
        #Saving data f
        #self.saveDataf(nameSave2, coordHA, i)
        if self.nbTarget == 0:
            sizeTarget = self.rs.sizeOfTarget[0]
        elif self.nbTarget == 4:
            #sizeTarget = self.fr.getobjread("targetSizeTmp")
            sizeTarget = self.targetSizeS
        if((coordHA[0] >= (0-sizeTarget/2) and coordHA[0] <= (0+sizeTarget/2)) and coordHA[1] >= (self.rs.targetOrdinate - self.rs.errorPosEnd)):
            Ju += self.rs.rhoCF
        self.costSave[nameSave2] = Ju
        return Ju
    


    def trajGenWithU(self, U, save):
#Thomas: commenter cette méthode
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



