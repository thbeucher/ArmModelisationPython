'''
Author: Thomas Beucher

Module: CreatePosIni

Description: Script for creating the initials positions
'''

import numpy as np
import math
from ArmModel.GeometricModel import mgi, mgd
import matplotlib.pyplot as plt
from Utils.FileReading import FileReading
from Utils.ReadSetupFile import ReadSetupFile
from Utils.FileSaving import fileSavingStr


def createPos():
    fr = FileReading()
    rs = ReadSetupFile()
    posi = fr.getobjread(rs.experimentFilePosIni)
    posx, posy = [], []
    for el in posi:
        posx.append(el[0])
        posy.append(el[1])
    
    x0, y0, = 0, 0.6175
    t = np.arange(7*math.pi/6, 11*math.pi/6, 0.1)
    r = np.arange(0.1, 0.5, 0.03)
    x, y, xy = [], [], []
    for i in range(t.shape[0]-1):
        for j in range(r.shape[0]):
            xt = x0 + r[j] * math.cos(t[i+1])
            yt = y0 + r[j] * math.sin(t[i+1])
            x.append(xt)
            y.append(yt)
            xy.append((xt, yt))
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(posx, posy, c = 'r')
    plt.show()
    Q = []
    for el in xy:
        Q.append(mgi(el[0], el[1], 0.3, 0.35))
    fileSavingStr("InitialPositionForBrent", Q)
    print(len(Q))
    








