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
from ArmModel.ArmDynamics import ArmDynamics, mdd, integration
from ArmModel.GeometricModel import mgi, mgd, jointStop
from ArmModel.SavingData import SavingData
import matplotlib.pyplot as plt
from matplotlib import animation


class SuperToolsInit:
    
    def __init__(self):
        '''
        class parameters initialization
        '''
        self.super = "SuperInit"
        self.save = SavingData()
        self.armP = ArmParameters()
        self.musclesP = MusclesParameters()
        self.armD = ArmDynamics()
        self.fr = FileReading()
        self.rs = ReadSetupFile()
        self.rs.readingSetupFile()
        #Initialisation des outils permettant d'utiliser le controleur rbfn
        self.fa = fa_rbfn(self.rs.numfeats)
        stateAll, commandAll = self.fr.recup_data(0)
        self.fa.setTrainingData(stateAll.T, commandAll.T)
        self.fa.setCentersAndWidths()
        #Recuperation des positions initiales de l'experimentation
        self.posIni = self.fr.getobjread("PosIniExperiment1")
    
    def initParamTraj(self):
        pass
    
    def costFunction(self, Ju, U, t):
        '''
        This function compute the cost of the trajectory
            
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
        Function which return the muscular activation vector U from the position vector Q
            
        Inputs:     -inputgc: (4,1) numpy array
                    -theta: 2D numpy array
        
        Outputs:    -Unoise: (6,1) numpy array, noisy muscular activation vector
        '''
        U = self.fa.functionApproximatorOutput(inputgc, theta)
        #Pas d'activations musculaires négatives possibles
        for i in range(U.shape[0]):
            if U[i] < 0:
                U[i] = 0
            elif U[i] > 1:
                U[i] = 1
        #Bruit d'activation musculaire 
        UnoiseTmp = U*(1+np.random.normal(0,self.rs.knoiseU))
        for i in range(UnoiseTmp.shape[0]):
            if UnoiseTmp[i] < 0:
                UnoiseTmp[i] = 0
            elif UnoiseTmp[i] > 1:
                UnoiseTmp[i] = 1
        Unoise = np.array([UnoiseTmp]).T
        return Unoise
        
    def trajGenerator(self, xI, yI, theta):
        '''
        This function generate the trajectory depend of the starting point given
        
        Inputs:     -xI: scalar, absciss of the trajectory starting point
                    -yI: scalar, ordinate of the trajectory starting point
                    -Theta: Numpy array
                    
        Output:    -Ju: scalar, cost of the trajectory
        '''
        q1, q2 = mgi(xI, yI, self.armP.l1, self.armP.l2)
        q = np.array([[q1], [q2]])
        dotq = self.armD.dotq0
        coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
        self.save.SaveTrajectory(coordEL, coordHA)
        t, i, Ju = 0, 0, 0#Ju = cost
        
        while coordHA[1] < self.rs.targetOrdinate:
            if i < 400:
                inputQ = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
                U = self.getCommand(inputQ, theta)
                ddotq = mdd(q, dotq, U, self.armP, self.musclesP)
                dotq, q = integration(dotq, q, ddotq, self.rs.dt)
                q = jointStop(q)
                coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
                self.save.SaveTrajectory(coordEL, coordHA)
                Ju = self.costFunction(Ju, U, t)
            else:
                break
            i += 1
            t += self.rs.dt
        print(i)
        if((coordHA[0] >= (0-self.rs.sizeOfTarget/2) and coordHA[0] <= (0+self.rs.sizeOfTarget/2)) and coordHA[1] >= self.rs.targetOrdinate):
            Ju += self.rs.rhoCF
        return Ju
    
    def trajGenWithU(self, U, save):
        q = np.array([[np.pi/2], [0]])
        dotq = self.armD.dotq0
        coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
        save.SaveTrajectory(coordEL, coordHA)
        t = 0
        while t <= 1:
            ddotq = mdd(q, dotq, U, self.armP, self.musclesP)
            dotq, q = integration(dotq, q, ddotq, self.rs.dt)
            coordEL, coordHA = mgd(q, self.armP.l1, self.armP.l2)
            save.SaveTrajectory(coordEL, coordHA)
            q = jointStop(q)
            t += self.rs.dt


#Le ccode qui suit permet de faire des test unitaires sur chaque muscles du bras
'''save = SavingData()

sti = SuperToolsInit()
U = sti.musclesP.activationVectorUse(0., 0., 0., 0., 0., 0.)
sti.trajGenWithU(U, save)
        
save.createCoord()

fig = plt.figure()
upperArm, = plt.plot([],[]) 
foreArm, = plt.plot([],[])
plt.xlim(-0.7, 0.7)
plt.ylim(-0.7,0.7)

def init():
    upperArm.set_data([0],[0])
    foreArm.set_data([save.xEl[0]],[save.yEl[0]])
    return upperArm,foreArm,

def animate(i): 
    xe = (0, save.xEl[i])
    ye = (0, save.yEl[i])
    xh = (save.xEl[i], save.xHa[i])
    yh = (save.yEl[i], save.yHa[i])
    upperArm.set_data(xe, ye)
    foreArm.set_data(xh, yh)
    return upperArm,foreArm
 
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=200, blit=True, interval=20, repeat=True)

plt.show(block=True)'''
        
