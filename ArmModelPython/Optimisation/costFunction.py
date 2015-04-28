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
from multiprocessing.sharedctypes import Array
from Script.MultiCoreComputeTraj import computeTraj
    
    
def costFunctionRBFN(theta):
    '''
    Compute the cost of each trajectories selected
    
    Input:      -theta: numpy array
    
    OutPuts:    -JuCf: list
                -sti: objet link
                -meanJu: numpy array, mean of the cost of each trajectories
    '''
    sti = SuperToolsInit()
    
    #Le nombre d'iteration pour i donne le nombre de trajectoire realises
    nbi = input("Nombre d'iteration a effectuer: ")
    nbi = int(nbi)
    
    data = sti.fr.getobjread(sti.rs.experimentFilePosIni)
    n = len(data)
    costf = []
    for i in range(int(nbi/4)):
        cost = []
        processUsed = []
        for j in range(4):
            cost.append(Array('d', range(n)))
            p = Process(target=computeTraj, args=(cost[j], sti, theta))
            processUsed.append(p)
        for j in range(4):
            processUsed[j].start()
        for j in range(4):
            processUsed[j].join()
        costTmp = np.vstack((cost[0], cost[1], cost[2], cost[3]))
        meanCostTmp = np.mean(costTmp, axis = 0)
        costf.append(meanCostTmp)
    meanf = np.mean(costf, axis = 0)
    return sti, meanf


class costFunctionClass:
    
    def __init__(self):
        self.call = 0
        self.sti = SuperToolsInit()
    
    def initTheta(self, theta):
        theta = unNorm(theta)
        self.theta = vectorToMatrix(theta)
        
    def serie1(self, JuS1):
        i = 0
        for el in self.sti.posIni:
            Ju = self.sti.trajGenerator(el[0], el[1], self.theta)
            JuS1[i] = Ju*(-1)
            i += 1
            
    def serie2(self, JuS2):
        i = 0
        for el in self.sti.posIni:
            Ju = self.sti.trajGenerator(el[0], el[1], self.theta)
            JuS2[i] = Ju*(-1)
            i += 1
            
    def serie3(self, JuS3):
        i = 0
        for el in self.sti.posIni:
            Ju = self.sti.trajGenerator(el[0], el[1], self.theta)
            JuS3[i] = Ju*(-1)
            i += 1
            
    def serie4(self, JuS4):
        i = 0
        for el in self.sti.posIni:
            Ju = self.sti.trajGenerator(el[0], el[1], self.theta)
            JuS4[i] = Ju*(-1)
            i += 1
              
    def costFunctionCMAES(self, theta):
        self.initTheta(theta)
        data = self.sti.fr.getobjread(self.sti.rs.experimentFilePosIni)
        n = len(data)
        
        JuS1, JuS2, JuS3, JuS4 = Array('d', range(n)), Array('d', range(n)), Array('d', range(n)), Array('d', range(n))
        p1, p2, p3, p4 = Process(target=self.serie1, args=(JuS1,)), Process(target=self.serie2, args=(JuS2,)), Process(target=self.serie3, args=(JuS3,)), Process(target=self.serie4, args=(JuS4,))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        
        juf = np.vstack((JuS1, JuS2, JuS3, JuS4))
        meanJuf = np.mean(juf, axis = 0)
        #print("meanjuf", meanJuf)
        JuSca = np.mean(meanJuf)
        print("Appel n°", self.call)
        self.call += 1
        print("Cout: ", JuSca)
        return JuSca



