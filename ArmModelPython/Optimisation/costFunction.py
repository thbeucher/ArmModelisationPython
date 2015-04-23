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
    
    
def costFunctionRBFN(theta):
    '''
    This function compute the cost of each trajectories selected
    
    Input:      -theta: numpy array
    
    OutPuts:    -JuCf: list
                -sti: objet link
                -meanJu: numpy array, mean of the cost of each trajectories
    '''
    sti = SuperToolsInit()
    Jutmp = {}
    
    #Ce bout de code permet de generer avec le controleur toutes les trajectoires sur lesquelles il a appris
    '''data, junk = sti.fr.recup_pos_ini(sti.rs.pathFolderTrajectories)
    for key, el in data.items():
        Ju = sti.trajGenerator(el[0], el[1], theta)
        JuCf.append((key, Ju))'''
    '''posi = []
    for i in range(10):
        posi.append(sti.posIni[7])'''
    #Le nombre d'iteration pour i donne le nombre de trajectoire realises
    nbi = input("Nombre d'iteration a effectuer: ")
    nbi = int(nbi)
    for i in range(nbi):
        JuCf = []
        for el in sti.posIni:
        #for el in posi:
            Ju = sti.trajGenerator(el[0], el[1], theta)
            #print(sti.save.coordHaSave[len(sti.save.coordHaSave)-1])
            JuCf.append(Ju)
        Jutmp[i] = JuCf
    s = 0
    for el in Jutmp.values():
        if s == 0:
            juju = np.array(el)
            s += 1
        else:
            juju = np.vstack((juju, el))
    meanJu = np.mean(np.array([juju]).T, axis = 1)
    return sti, meanJu


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
        
        JuS1, JuS2, JuS3, JuS4 = Array('d', range(12)), Array('d', range(12)), Array('d', range(12)), Array('d', range(12))
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
        print("meanjuf", meanJuf)
        JuSca = np.mean(meanJuf)
        print("Appel n°", self.call)
        self.call += 1
        print("Cout: ", JuSca)
        return JuSca



