'''
Author: Thomas Beucher

Module: VectorField 

Description: We find here script which print the moving vector for some point of space
'''

import numpy as np
import matplotlib.pyplot as plt
from ArmModel.GeometricModel import mgi, mgd
from Main.GenerateTrajectory import GenerateTrajectory
from ArmModel.ArmDynamics import mdd


def vectorField():
    #theta recovery
    sti = GenerateTrajectory()
    nameT = "RBFN2/" + str(sti.rs.numfeats) + "feats/"
    theta = sti.fr.getobjread(nameT + "ThetaX7BIN")
    sti.setTheta(theta)
    #Creation of some points of SPACE
    x = np.arange(-0.15, 0.16, 0.02)
    y = np.arange(0.5, 0.61, 0.02)
    p, pq = [], []
    for i in range(len(x)):
        for j in range(len(y)):
            p.append((x[i], y[j]))
            pq.append(mgi(x[i], y[j], sti.armP.l1, sti.armP.l2))
    #recovery of the next position for each points
    coord = []
    for el in pq:
        inputQ = np.array([[0], [0], [el[0]], [el[1]]])
        U = sti.NS.GC.getCommand(inputQ, theta)
        ddotq, dotq, q = mdd(np.array([[el[0]], [el[1]]]), np.array([[0], [0]]), U, sti.armP, sti.musclesP, 0.02)
        coordEL, coordHA = mgd(q, sti.armP.l1, sti.armP.l2)
        coord.append(coordHA)
    px, py = [], []
    for el in p:
        px.append(el[0])
        py.append(el[1])
    pxn, pyn = [], []
    for el in coord:
        pxn.append(el[0])
        pyn.append(el[1])
    plt.figure()
    plt.scatter(0, sti.rs.targetOrdinate, c = "r", marker=u'*', s = 100)
    plt.scatter(px, py, c = 'b')
    plt.scatter(pxn, pyn, c = 'r')
    for i in range(len(p)):
        if abs(p[i][0] - coord[i][0]) != 0 and abs(p[i][1] - coord[i][1]) != 0:
            plt.annotate("", xy=(coord[i][0], coord[i][1]), xytext=(p[i][0], p[i][1]), arrowprops=dict(arrowstyle="->"))
    plt.show()
    
    
vectorField()




