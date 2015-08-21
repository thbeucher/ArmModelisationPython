'''
Author: Thomas Beucher
Module: FindPosIniOutSolv
'''
import sys
name = "/home/beucher/ProjetCluster/ArmModelPython/"
sys.path.append(name + "Utils")
sys.path.append(name + "ArmModel")
sys.path.append(name + "Main")
sys.path.append(name + "Regression")
sys.path.append(name + "Script")
sys.path.append(name + "Optimisation")

import os
import matplotlib.pyplot as plt
import numpy as np

def calculCoord(q):
    l1,l2 = 0.3,0.35
    coordHand = (l2*np.cos(q[1,0] + q[0,0]) + l1*np.cos(q[0,0]), l2*np.sin(q[1,0] + q[0,0]) + l1*np.sin(q[0,0]))
    return coordHand

def allpts():
    q1 = np.arange(-0.6,2.6,0.3)
    q2 = np.arange(-0.2,3.0,0.3)
    Q1,Q2 = np.meshgrid(q1,q2)
    cor = []
    for i in range(Q1.shape[0]):
        for j in range(Q1.shape[1]):
            corH = calculCoord(np.mat([[Q1[i,j]],[Q2[i,j]]]))
            cor.append(corH)
    corx, cory = [], []
    for el in cor:
        corx.append(el[0])
        cory.append(el[1])
    return corx,cory

def runfpios():
    patho = "/home/beucher/Desktop/Monfray/Codes/Java/output_solver/"
    elsplit = []
    for el in os.listdir(patho):
        if not "fail" in el and not "junk" in el:
            elsplit.append(el.split("_"))
    
    
    cor = []
    for el in elsplit:
        cor.append(calculCoord(np.mat([[float(el[2])],[float(el[3])]])))
    
    corx,cory = [],[]
    for el in cor:
        corx.append(el[0])
        cory.append(el[1])
    
    corxA, coryA = allpts()
    
    plt.figure()
    plt.scatter(corx, cory, c ='b')
    plt.figure()
    plt.scatter(corxA, coryA, c = 'b')
    plt.show()
    
#runfpios()
