'''
Author: Thomas Beucher

Module: costFunction

Description: We find here the function which allow to evaluate the cost of each trajectories
'''
import numpy as np
import time
from Utils.ThetaNormalization import vectorToMatrix, unNorm
from Main.SuperToolsInit import SuperToolsInit
from multiprocessing.context import Process
from multiprocessing.sharedctypes import Array, Value
from Script.MultiCoreComputeTraj import computeTraj
from Utils.FileSaving import fileSavingBin
from multiprocessing.pool import ThreadPool
    

class costFunctionClass:
    #Thomas: c'est quoi, serie1 à serie4 ? Moche... => renommer et revoir
    def __init__(self, nbtarget = 0, targetSize = 0):
        self.call = 0
        self.targetS = targetSize
        self.sti = SuperToolsInit(nbtarget, targetSize)
        #self.startPTs, junk = self.sti.fr.recup_pos_ini(self.sti.rs.pathFolderTrajectories)
        #self.n = len(self.startPTs)
        self.n = len(self.sti.posIni)
        self.saveCost = []
    
    def initTheta(self, theta):
        theta = vectorToMatrix(theta)
        self.theta = unNorm(theta)
            
    def threadingCmaes(self, cost):
        for el in self.sti.posIni:
            costTmp = self.sti.trajGenerator(el[0], el[1], self.theta)
            cost.append(costTmp)
        return cost
              
    def costFunctionCMAES(self, theta):
        #Thomas: commenter cette méthode
        self.initTheta(theta)
        '''c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = [], [], [], [], [], [], [], [], [], []
        pool = ThreadPool(10)
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10= pool.map(self.threadingCmaes, [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])
        resC = np.vstack((c1, c2, c3, c4, c5, c6, c7, c8, c9, c10))
        meanResC = np.mean(resC, axis = 0)
        meanT = np.mean(meanResC)
        print("Appel n°", self.call)
        self.call += 1
        print("Cout: ", meanT)
        pool.terminate()
        self.sti.initParamTraj()
        self.saveCost.append(meanT)
        if self.call == (self.sti.rs.maxIterCmaes * self.sti.rs.popsizeCmaes):
            sizeTargetTmp = self.targetS
            namet = "OptimisationResults/costEval" + str(sizeTargetTmp)
            print("saveCost: ", len(self.saveCost))
            fileSavingBin(namet, self.saveCost)
        return meanT*(-1)'''
        
        costT = {}
        for i in range(5):
            JuS = []
            for el in self.sti.posIni:
                Ju = self.sti.trajGenerator(el[0], el[1], self.theta)
                JuS.append(Ju)
            costT[i] = JuS
        s = 0
        for el in costT.values():
            if s == 0:
                costArray = el
                s += 1
            else:
                costArray = np.vstack((costArray, el))
        meanJuf = np.mean(costArray, axis = 0)
        #print("meanjuf", meanJuf)
        JuSca = np.mean(meanJuf)
        print("Appel n°", self.call)
        self.call += 1
        print("Cout: ", JuSca)
        self.sti.initParamTraj()
        self.saveCost.append(JuSca)
        if self.call == (self.sti.rs.maxIterCmaes * self.sti.rs.popsizeCmaes):
            sizeTargetTmp = self.targetS
            namet = "OptimisationResults/costEval" + str(sizeTargetTmp)
            print("saveCost: ", len(self.saveCost))
            fileSavingBin(namet, self.saveCost)
        return JuSca*(-1)
    
    def costFunctionRBFN(self, theta):
        '''
        Computes the cost of each selected trajectory
        
        Input:      -theta: numpy array
        
        OutPuts:    -JuCf: list
                    -sti: objet link
                    -meanJu: numpy array, mean of the cost of each trajectories
        '''
        costT = {}
        #Le nombre d'iteration pour i donne le nombre de trajectoire realises
        nbi = input("Nombre d'iteration a effectuer: ")
        nbi = int(nbi)
        
        #startPTs, junk = sti.fr.recup_pos_ini(sti.rs.pathFolderTrajectories)
        
        for i in range(nbi):
            JuS = []
            for el in self.sti.posIni:
            #for el in startPTs.values():
                Ju = self.sti.trajGenerator(el[0], el[1], theta)
                JuS.append(Ju)
            costT[i] = JuS
        s = 0
        for el in costT.values():
            if s == 0:
                costArray = el
                s += 1
            else:
                costArray = np.vstack((costArray, el))
        if nbi > 1:
            meanJu = np.mean(costArray, axis = 0)
        else:
            meanJu = costArray
        return self.sti, meanJu




