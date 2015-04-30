'''
Author: Thomas Beucher

Module: CreatePosIni

Description: Script for creating the initials positions
'''

import numpy as np
import math
from ArmModel.GeometricModel import mgi, mgd
import matplotlib.pyplot as plt
from Utils.NiemRoot import tronquerNB
from Utils.InitUtil import initFRRS
import os


def createPos():
    fr, rs = initFRRS()
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
            x.append(tronquerNB(xt, 6))
            y.append(tronquerNB(yt, 6))
            xy.append((xt, yt))
    
    rt1 = np.arange(0.37, 0.5, 0.03)
    tt1 = np.arange(7*math.pi/6 + 0.1, 11*math.pi/6 - 0.05, 0.05)     
    xt1, yt1, xyt1 = [], [], []
    for i in range(tt1.shape[0]):
        for j in range(rt1.shape[0]):
            xr = x0 + rt1[j] * math.cos(tt1[i])
            yr = y0 + rt1[j] * math.sin(tt1[i])
            if tronquerNB(xr, 6) not in x and tronquerNB(yr, 6) not in y:
                xt1.append(tronquerNB(xr, 6))
                yt1.append(tronquerNB(yr, 6))
                xyt1.append((tronquerNB(xr, 6), tronquerNB(yr, 6)))
    
    rt11 = np.arange(0.28, 0.37, 0.03)
    tt11 = np.arange(7*math.pi/6 + 0.1, 11*math.pi/6 - 0.05, 0.05)
    xt11, yt11, xyt11 = [], [], []
    for i in range(tt11.shape[0]):
        for j in range(rt11.shape[0]):
            xr1 = x0 + rt11[j] * math.cos(tt11[i])
            yr1 = y0 + rt11[j] * math.sin(tt11[i])
            if tronquerNB(xr1, 6) not in x and tronquerNB(yr1, 6) not in y:
                xt11.append(tronquerNB(xr1, 6))
                yt11.append(tronquerNB(yr1, 6))
                xyt11.append((tronquerNB(xr1, 6), tronquerNB(yr1, 6)))
                
    rt12 = np.arange(0.25, 0.26, 0.03)
    tt12 = np.arange(7*math.pi/6 + 0.1, 11*math.pi/6 - 0.05, 0.05)
    xt12, yt12, xyt12 = [], [], []
    for i in range(tt12.shape[0]):
        for j in range(rt12.shape[0]):
            xr2 = x0 + rt12[j] * math.cos(tt12[i])
            yr2 = y0 + rt12[j] * math.sin(tt12[i])
            if tronquerNB(xr2, 6) not in x and tronquerNB(yr2, 6) not in y and yr2 < 0.4:
                xt12.append(tronquerNB(xr2, 6))
                yt12.append(tronquerNB(yr2, 6))
                xyt12.append((tronquerNB(xr2, 6), tronquerNB(yr2, 6)))
    
    d1 = np.arange(-0.10, 0.07, 0.01)
    d2 = np.arange(0.12, 0.25, 0.01)    
    d11 = np.arange(0.08, 0.14, 0.01)
    d22 = np.arange(0.15, 0.23, 0.01)  
    d111 = np.arange(0.16, 0.25, 0.01)
    d222 = np.arange(0.16, 0.20, 0.01)
    xx, yy, xyt = [], [], []
    for i in range(len(d1)):
        for j in range(len(d2)):
            xx.append(d1[i])
            yy.append(d2[j])
            xyt.append((tronquerNB(d1[i],5), tronquerNB(d2[j],5)))
    for i in range(len(d11)):
        for j in range(len(d22)):
            xx.append(d11[i])
            yy.append(d22[j])
            xyt.append((tronquerNB(d11[i], 5), tronquerNB(d22[j], 5)))
    for i in range(len(d111)):
        for j in range(len(d222)):
            xx.append(d111[i])
            yy.append(d222[j])
            xyt.append((tronquerNB(d111[i], 5), tronquerNB(d222[j], 5)))
    #fileSavingStr("coucou", xyt)
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(posx, posy, c = 'r')
    
    plt.scatter(xt1, yt1, c = 'y')
    plt.scatter(xt11, yt11, c = "m")
    plt.scatter(xt12, yt12, c = 'y')
    #plt.scatter(xx, yy, c = 'y')
    
    plt.show()
    Q = []
    for el in xy:
        Q.append(mgi(el[0], el[1], 0.3, 0.35))
    #fileSavingStr("InitialPositionForBrent", Q)
    Qt = []
    for el in xyt1:
        Qt.append(mgi(el[0], el[1], 0.3, 0.35))
    print(Qt)
    print(len(Q))
    Qt1 = []
    for el in xyt11:
        Qt1.append(mgi(el[0], el[1], 0.3, 0.35))
    print(Qt1)
    Qt2 = []
    for el in xyt12:
        Qt2.append(mgi(el[0], el[1], 0.3, 0.35))
    print(Qt2)
    
def create2():
    fr, rs = initFRRS()
    ###
    Q = []
    name1 = "/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/"
    for el in os.listdir(name1):
        if "brentbvp" in el and not "fail" in el:
            Q.append(el)
    x1, y1, xy1 = [], [], []
    for el in Q:
        x1.append(float((el.split("_")[2])))
        y1.append(float((el.split("_")[3])))
        xy1.append((float((el.split("_")[2])), float(el.split("_")[3])))
    ###
    posi = fr.getobjread(rs.experimentFilePosIni)
    posx, posy = [], []
    for el in posi:
        posx.append(el[0])
        posy.append(el[1])
        
    x = np.arange(-0.3, 0.31, 0.01)
    y = np.arange(0.2, 0.61, 0.01)
    xx, yy, xyt = [], [], []
    for i in range(len(x)):
        for j in range(len(y)):
            xx.append(x[i])
            yy.append(y[j])
            xyt.append((tronquerNB(x[i], 5), tronquerNB(y[j], 5)))
    
    q1, q2, q3, q4, qt = [], [], [], [], []
    for el in xyt:
        a = mgi(el[0], el[1], 0.3, 0.35)
        if not a == "None":
            qt.append(mgi(el[0], el[1], 0.3, 0.35))
            if len(q1) < 620:
                q1.append(mgi(el[0], el[1], 0.3, 0.35))
            elif len(q2) < 620:
                q2.append(mgi(el[0], el[1], 0.3, 0.35))
            elif len(q3) < 620:
                q3.append(mgi(el[0], el[1], 0.3, 0.35))
            else:
                q4.append(mgi(el[0], el[1], 0.3, 0.35))
    
    qx, qy = [], []
    for el in qt:
        qx.append(el[0])
        qy.append(el[1])
    
    xf, yf, xyf = [], [], []
    qxt = qx
    for el in qt:
        if not el in xy1:
            xf.append(el[0])
            yf.append(el[1])
            xyf.append(el)
    print(len(xyf), xyf)
    print(len(qt))
    print(len(xx))
    
    plt.figure()
    plt.scatter(posx, posy, c = 'b')
    plt.scatter(0, rs.targetOrdinate, marker=u'*', s = 100)
    plt.scatter(xx, yy, c = 'r')
    plt.show()
    

#create2()
#createPos()
#Le code qui suit permet de generer les positions initiales pour les trajectoires proches de la cible
'''x = np.arange(-0.08, 0.09, 0.02)
y = np.arange(0.59, 0.617, 0.01)
c, cx, cy = [], [], []
for i in range(len(x)):
    for j in range(len(y)):
        c.append((x[i], y[j]))
for el in c:
    cx.append(el[0])
    cy.append(el[1])
plt.figure()
plt.scatter(0, 0.6175, c = "r", marker=u'*', s = 100)
plt.scatter(cx, cy, c = 'b')
plt.show()

q = []
for el in c:
    q.append(mgi(el[0], el[1], 0.3, 0.35))
print(q)'''



