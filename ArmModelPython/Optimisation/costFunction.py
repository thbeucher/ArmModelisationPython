#######################################################################################
########## Author: Thomas Beucher // Module: costFunction #############################
#######################################################################################
from math import sqrt
import numpy as np
import time
from FileProcessing.FileReading import FileReading
from ArmModel.ParametresArmModel import ParametresArmModel
from ArmModel.ParametresHogan import ParametresHogan
from ArmModel.ParametresRobot import ParametresRobot
from Regression.ControlerUtil import ControlerUtil
from ArmModel.SavingData import SavingData
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
from Regression.functionApproximator_RBFN import fa_rbfn
import math as m

class costFunction:
    
    def __init__(self, inb = 0):
        self.gamma = 0.998
        self.rho = 10
        self.ups = 3000
        self.Ju = 0
        self.suivi = 0
        self.inb = inb
        
    def costFunctionJ(self, U, action, t):
        usquare = np.square(U)
        usum = 0
        for el in usquare:
            usum += el
        mvtCost = (sqrt(usum))**2
        if action == 1:
            imReward = 0
        else:
            imReward = 1
        self.Ju += np.exp(-t/self.gamma)*(self.rho*imReward - self.ups*mvtCost)
        
    
    def costFunctionRBFN2(self, theta):
        t0 = time.time()
        #Déclaration des différentes classes utiles 
        robot = ParametresRobot()
        hogan = ParametresHogan()
        arm = ParametresArmModel(hogan.GammaMax)
        save = SavingData()
        fr = FileReading()
        #Remise sous forme de matrice de theta (quand lancer avec cmaes
        #Pour l'instant non générique, changer nb(nbfeat**nbdim) pour correspondre au bon theta
        nbf = 3
        nbd = 4
        nbt = 0
        coordStartPts = []
        coordStartPts.append((-0.2,0.39))#trajectoire1
        coordStartPts.append((-0.1,0.39))#trajectoire2
        coordStartPts.append((0.0,0.39))#trajectoire3
        coordStartPts.append((0.1,0.39))#trajectoire4
        coordStartPts.append((0.2,0.39))#trajectoire5
        coordStartPts.append((-0.3,0.0325))#trajectoire6
        coordStartPts.append((-0.2,0.0325))#trajectoire7
        coordStartPts.append((-0.1,0.0325))#trajectoire8
        coordStartPts.append((0.0,0.0325))#trajectoire9#0000
        coordStartPts.append((0.1,0.0325))#trajectoire10
        coordStartPts.append((0.2,0.0325))#trajectoire11
        coordStartPts.append((0.3,0.0325))#trajectoire12
        JuCf = []
        if self.inb == 1:
            stateAll, commandAll = fr.recup_data(1)
        elif self.inb == 0:
            stateAll, commandAll = fr.recup_data(0)
        fa = fa_rbfn(nbf)
        fa.setTrainingData(stateAll.T, commandAll.T)
        fa.setCentersAndWidths()
        cu = ControlerUtil(nbf,nbd)
        ############################################################
        ##For saving U and coordTraj and Unoise
        #y = 0
        ##Pour sauvegarder le nombre d'iteration pour resoudre les trajectoires
        #savei = []
        ##avec noise
        #namei = "RBFN2/" + str(nbf) + "feats/nbIteTraj"
        #nameinoise = "RBFN2/" + str(nbf) + "feats/nbIteTrajNoise"
        ############################################################
        for el in coordStartPts:
            #print("x:", el[0], "\ny:", el[1])
            q1, q2 = fr.convertToAngle(el[0], el[1], robot) 
            #print("q1:", q1, "\nq2:", q2)
            q = np.array([[q1],[q2]])
            dotq = np.array([[0.],[0.]])
            coordEL, coordHA = save.calculCoord(q, robot)
            #print("coordHA:",coordHA)
            i = 0
            arm.t = 0
            self.Ju = 0
            ############################################################
            ##For saving U
            #saveU = []
            #y += 1
            #nameU = "RBFN2/" + str(nbf) + "feats/ActiMuscuTrajectoire" + str(y+1)
            ##For saving Unoise
            #saveU = []
            #nameUnoise = "RBFN2/" + str(nbf) + "feats/ActiMuscuNoiseTrajectoire" + str(y+1)
            #y += 1
            ##For saving coord Traj
            #nameCoordEL = "RBFN2/" + str(nbf) + "feats/CoordTraj/CoordTrajectoireEL" + str(12)
            #nameCoordHA = "RBFN2/" + str(nbf) + "feats/CoordTraj/CoordTrajectoireHA" + str(12)
            ##For saving all coord traj
            #nameCoordEL = "RBFN2/" + str(nbf) + "feats/CoordTraj/CoordTrajectoireELAll"
            #nameCoordHA = "RBFN2/" + str(nbf) + "feats/CoordTraj/CoordTrajectoireHAAll"
            ##For saving all coord traj noise
            #nameCoordEL = "RBFN2/" + str(nbf) + "feats/CoordTraj/CoordTrajectoireELAllNoise"
            #nameCoordHA = "RBFN2/" + str(nbf) + "feats/CoordTraj/CoordTrajectoireHAAllNoise"
            ############################################################
            while coordHA[1] < 0.6175:
                if i < 900:
                    inputq = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
                    cu.getCommand(inputq, nbt, fa, theta)
                    ##############################
                    ##For saving U and Unoise
                    #saveU.append(cu.U)
                    ##############################
                    Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*(np.array([cu.U]).T)#without noise
                    #Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*(np.array([cu.Unoise]).T)#With Noise
                    ddotq = arm.MDD( Gamma_AM,q,dotq,robot)
                    dotq += ddotq*arm.dt
                    q += dotq*arm.dt
                    coordEL, coordHA = save.calculCoord(q, robot)
                    ##############################
                    ##For saving coordTraj
                    #save.SaveTrajectory(coordEL, coordHA)
                    ##############################
                    if coordHA[0] == 0.0 and coordHA[1] == 0.6175:
                        self.costFunctionJ(cu.U, 2, arm.t)
                    else:
                        self.costFunctionJ(cu.U, 1, arm.t)
                else:
                    break
                i += 1
                arm.t += arm.dt
            ##############################
            ##For saving U
            #fileSavingBin(nameU, saveU)
            ##For saving Unoise
            #fileSavingBin(nameUnoise, saveU)
            ##Pour sauvegarder le nombre d'iteration pour resoudre les trajectoires
            #savei.append(i)
            ##For saving coordTraj
            #print("len", len(save.coordHaSave))
            #fileSavingBin(nameCoordEL, save.coordElSave)
            #fileSavingBin(nameCoordHA, save.coordHaSave)
            ##############################
            print(i)
            JuCf.append(self.Ju*(-1))
        ###########################################
        ##Pour sauvegarder toutes les coordonnes
        #fileSavingBin(nameCoordEL, save.coordElSave)
        #fileSavingBin(nameCoordHA, save.coordHaSave)
        ##Pour sauvegarder le nombre d'iteration pour resoudre les trajectoires
        #fileSavingStr(namei, savei)
        ##Pour sauvegarder le nombre d'iteration pour resoudre les trajectoires noise
        #fileSavingStr(nameinoise, savei)
        ###########################################
        fileSavingStr("CalculCoutTest", JuCf)
        self.suivi += 1
        t1 = time.time()
        print("Fin d'appel! (", self.suivi, ") (Temps de traitement:", (t1-t0), "s)")
        return JuCf
    
    
    
    
    def costFunctionCMAES(self, theta):
        t0 = time.time()
        #Déclaration des différentes classes utiles 
        robot = ParametresRobot()
        hogan = ParametresHogan()
        arm = ParametresArmModel(hogan.GammaMax)
        save = SavingData()
        fr = FileReading()
        #Remise sous forme de matrice de theta (quand lancer avec cmaes
        #Pour l'instant non générique, changer nb(nbfeat**nbdim) pour correspondre au bon theta
        nb = 0
        for i in range(int(theta.shape[0]/6)):
            thetaTmp = []
            for j in range(6):
                thetaTmp.append(theta[j + nb])
            if i == 0:
                thetaf = np.array([thetaTmp])
            else:
                thetaf = np.vstack((thetaf, np.array([thetaTmp])))
            nb += 6
        theta = thetaf
        nbf = 3
        nbd = 4
        nbt = 0
        coordStartPts = []
        coordStartPts.append((-0.2,0.39))#trajectoire1
        coordStartPts.append((-0.1,0.39))#trajectoire2
        coordStartPts.append((0.0,0.39))#trajectoire3
        coordStartPts.append((0.1,0.39))#trajectoire4
        coordStartPts.append((0.2,0.39))#trajectoire5
        coordStartPts.append((-0.3,0.0325))#trajectoire6
        coordStartPts.append((-0.2,0.0325))#trajectoire7
        coordStartPts.append((-0.1,0.0325))#trajectoire8
        coordStartPts.append((0.0,0.0325))#trajectoire9#0000
        coordStartPts.append((0.1,0.0325))#trajectoire10
        coordStartPts.append((0.2,0.0325))#trajectoire11
        coordStartPts.append((0.3,0.0325))#trajectoire12
        JuCf = []
        stateAll, commandAll = fr.recup_data(0)
        fa = fa_rbfn(nbf)
        fa.setTrainingData(stateAll.T, commandAll.T)
        fa.setCentersAndWidths()
        cu = ControlerUtil(nbf,nbd)
        for el in coordStartPts:
            q1, q2 = fr.convertToAngle(el[0], el[1], robot) 
            q = np.array([[q1],[q2]])
            dotq = np.array([[0.],[0.]])
            coordEL, coordHA = save.calculCoord(q, robot)
            i = 0
            arm.t = 0
            self.Ju = 0
            while coordHA[1] < 0.6175:
                if i < 900:
                    inputq = np.array([[dotq[0,0]], [dotq[1,0]], [q[0,0]], [q[1,0]]])
                    cu.getCommand(inputq, nbt, fa, theta)
                    #Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*(np.array([cu.U]).T)#without noise
                    Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*(np.array([cu.Unoise]).T)#With Noise
                    ddotq = arm.MDD( Gamma_AM,q,dotq,robot)
                    dotq += ddotq*arm.dt
                    q += dotq*arm.dt
                    coordEL, coordHA = save.calculCoord(q, robot)
                    if coordHA[0] == 0.0 and coordHA[1] == 0.6175:
                        self.costFunctionJ(cu.U, 2, arm.t)
                    else:
                        self.costFunctionJ(cu.U, 1, arm.t)
                else:
                    break
                i += 1
                arm.t += arm.dt
            print(i)
            JuCf.append(self.Ju*(-1))
        fileSavingStr("CalculCoutTest", JuCf)
        self.suivi += 1
        t1 = time.time()
        print("Fin d'appel! (", self.suivi, ") (Temps de traitement:", (t1-t0), "s)")
        return JuCf

