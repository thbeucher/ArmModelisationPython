'''
Author: Thomas Beucher

Module: costFunction

Description: We find here the function which allow to evaluate the cost of each trajectories
'''
import numpy as np
#import time
from Utils.ThetaNormalization import vectorToMatrix, unNorm
from Main.SuperToolsInit import SuperToolsInit
from multiprocessing.context import Process
#from multiprocessing.sharedctypes import Array, Value
from Utils.FileSaving import fileSavingBin
from multiprocessing.pool import ThreadPool
    

class costFunctionClass:
    #Thomas: c'est quoi, serie1 à serie4 ? Moche... => renommer et revoir
    def __init__(self, nbtarget = 0, targetSize = 0):
        self.call = 0
        self.targetS = targetSize
        self.sti = SuperToolsInit(nbtarget, targetSize)
        self.n = len(self.sti.posIni)
        self.saveCost = []
    
    def initTheta(self, theta):
        '''
        Initializes theta for cmaes processing, ie reshaping and un-norm
        
        Input:     -theta: numpy array, (x,)
        
        Output:    -self.theta: numpy array, (x1, y1) where x1 = number of features to the input dimension
                        and y1 = dimension of the output
        '''
        theta = vectorToMatrix(theta)
        self.theta = unNorm(theta)
            
    def threadingCmaes(self, cost):
        '''
        Used for the multithreading
        '''
        for el in self.sti.posIni:
            costTmp = self.sti.trajGenerator(el[0], el[1], self.theta)
            cost.append(costTmp)
        return cost
              
    def costFunctionCMAES(self, theta):
        '''
        evaluate each trajectories x time, get the cost for each, compute the mean for the x tries of each trajectories
        then compute the mean for all trajectories and return it to cmaes
        
        Input:     -theta: numpy array, (x,)
        
        Output:    -scalar, the mean of the cost of all trajectories
        '''
        #reshape and unNorm the theta
        self.initTheta(theta)
        #the code commented is the multithreading version
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
        #launch each trajectories x (here x = 5) times
        for i in range(5):
            JuS = []
            #posIni is an array with all initials points used for the experiment
            for el in self.sti.posIni:
                #trajGenerator is the function which compute the trajectory from the initial point given
                Ju = self.sti.trajGenerator(el[0], el[1], self.theta)
                #store the cost of trajectories
                JuS.append(Ju)
            costT[i] = JuS
        s = 0
        #compute the mean of the x tries for each trajectories
        for el in costT.values():
            if s == 0:
                costArray = el
                s += 1
            else:
                costArray = np.vstack((costArray, el))
        meanJuf = np.mean(costArray, axis = 0)
        #compute the mean of the cost of all trajectories
        JuSca = np.mean(meanJuf)
        print("Appel n°", self.call)
        self.call += 1
        print("Cout: ", JuSca)
        #dump old data from store of sti object
        self.sti.initParamTraj()
        #Save the cost of each tries of cmaes
        self.saveCost.append(JuSca)
        if self.call == (self.sti.rs.maxIterCmaes * self.sti.rs.popsizeCmaes):
            sizeTargetTmp = self.targetS
            namet = "OptimisationResults/costEvalAll/costEval" + str(sizeTargetTmp) + str(self.call)
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




