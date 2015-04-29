'''
Author: Thomas Beucher

Module: plotFunctions

Description: On retrouve dans ce fichier differentes fonctions permettant d'afficher les resultats du projet
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
from matplotlib.mlab import griddata
import mpl_toolkits
import os
from ArmModel.GeometricModel import mgi, mgd
import math
from Utils.NiemRoot import tronquerNB
from Utils.InitUtil import initFRRS
from Utils.FileReading import FileReading
from shutil import copyfile
from posix import remove
from Utils.FunctionsUsefull import returnX0Y0Z, returnDifCostBrentRBFN

def costColorPlot(wha):
    '''
    Cette fonction permet d'afficher le profil de cout des trajectoires
    
    Entrees:    -nbfeat: nombre de features utilises pour generer le controleur actuel
                -wha: choix des donnees a afficher
    '''
    xt = 0
    
    fr, rs = initFRRS()
    nbfeat = rs.numfeats
    
    xy0tmp, Q = fr.recup_pos_ini(rs.pathFolderTrajectories)
    x0 = []
    y0 = []
    posi = fr.getobjread(rs.experimentFilePosIni)
    for el in posi:
        x0.append(el[0])
        y0.append(el[1])
        
    if wha == "rbfn":
        name = "RBFN2/" + str(nbfeat) + "feats/"
        z = fr.getobjread(name + "costBIN")
        if len(z) > len(x0):
            x0, y0, z = returnX0Y0Z()
        maxt = np.max(np.abs(z))
        
    elif wha == "cma":
        name = "RBFN2/" + str(nbfeat) + "feats/costBINCma"
        z = fr.getobjread(name)
        for i in range(len(z)):
            if z[i] > 0:
                z[i] -= rs.rhoCF
        maxt = np.max(abs(z))
        
    elif wha == "brent":
        data = fr.getobjread("trajectoires_cout/trajectoire_coutCoordXBIN")
        z, x0, y0 = [], [], []
        for el in data:
            z.append(el[1]-rs.rhoCF)
            x0.append(el[2])
            y0.append(el[3])
        maxt = np.max(np.abs(z))
    
    elif wha == "difBR":
        dif = returnDifCostBrentRBFN()
        z, zobj, x0, y0 = [], [], [], []
        for el in dif:
            if el[2] < 10:
                z.append(el[2])
                zobj.append(el)
                x0.append(el[0])
                y0.append(el[1])
        
    
    #zb = z/maxt
    zb = z
    xi = np.linspace(-0.4,0.4,200)
    yi = np.linspace(0.1,0.6,200)
    er = 0
    try:
        zb.shape[1]
    except IndexError:
        er = 1
    except AttributeError:
        er = 1
    if type(zb) == type([]):
        print(x0, "\n", y0, "\n", zb)
        print(len(x0), len(y0), len(zb))
        zi = griddata(x0, y0, zb, xi, yi)
    elif er == 1:
        zi = griddata(x0, y0, zb, xi, yi)
    else:
        zi = griddata(x0, y0, zb.T[0], xi, yi)
    
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=zb, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, rs.targetOrdinate, c ='g', marker='v', s=200)
    CS = plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t1, shrink=0.5, aspect=5)
    
    plt.show(block = True)


def plotActivationMuscular(what):
    '''
    Cette fonction permet d'afficher les activations musculaires des trajectoires
    
    Entrees:    -wha: choix des donnees a afficher
                -nbfeat: nombre de features utilises pour generer le controleur actuel
                
    '''
    fr, rs = initFRRS()
    nbfeat = rs.numfeats
    if what == "brent":
        #BrentBVPSolver activations muscular
        pass
    elif what == "rbfn":
        nameR = "RBFN2/" + str(nbfeat) + "feats/Uall"
        coutTraj = fr.getobjread(nameR)
        dicoVal = {}
        for key, val in coutTraj.items():
            valu = np.array(val).T
            x = []
            for i in range(valu[0].shape[1]):
                x.append(i)
            rbfn = plt.figure()
            for i in range(valu[0].shape[0]):
                plt.plot(x, valu[0][i])
            plt.show(block = True)
        
    elif what == "cma":
        pass
    
def timeDistance():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/nbIteBIN" 
    data = fr.getobjread(name)
    key = []
    for el in data.keys():
        key.append(el.split("//"))
    for i in range(len(key)):
        key[i][0] = float(key[i][0])
        key[i][1] = float(key[i][1])
    r = []
    for el in key:
        r1 = math.sqrt(((tronquerNB(el[0], 5)**2) + ((tronquerNB(el[1], 5) - 0.6175)**2)))/2
        r.append(tronquerNB(r1, 2))
    

def hitDispersion():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/CoordHitTargetBIN" 
    data = fr.getobjread(name)
    tab = []
    for el in data.values():
        for el1 in el:
            tab.append(el1)
    tabx, taby = [], []
    for el in tab:
        tabx.append(el[0])
        taby.append(rs.targetOrdinate)
    plt.figure()
    plt.plot([-0.2, 0.2], [rs.targetOrdinate, rs.targetOrdinate], c = 'r')
    plt.scatter([-rs.sizeOfTarget/2, rs.sizeOfTarget/2], [rs.targetOrdinate, rs.targetOrdinate], marker=u'|', s = 100)
    plt.scatter(tabx, taby, c = 'b')
    plt.show(block = True)
    
def velocityProfile():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/SpeedSaveBIN" 
    data = fr.getobjread(name)
    
    

def plot_pos_ini():
    '''
    Cette fonction permet d'afficher les positions initiales des trajectoires
    (trajectoire disponible dans le dossier trajectoire)           
    '''
    x0 = []
    y0 = []
    fr, rs = initFRRS()
    xt = 0
    yt = rs.targetOrdinate
    posIni = fr.getobjread(rs.experimentFilePosIni)
    for el in posIni:
        x0.append(el[0])
        y0.append(el[1])
    xy, junk = fr.recup_pos_ini(rs.pathFolderTrajectories)
    x, y = [], []
    aa, keyy = [], []
    for key, el in xy.items():
        x.append(el[0])
        y.append(el[1])
        a = math.sqrt((el[0]**2) + (el[1] - 0.6175)**2)
        if tronquerNB(a, 3) not in aa:
            aa.append(tronquerNB(a, 3))
        if a < 0.11:
            keyy.append(key)
            #copyfile(rs.pathFolderTrajectories + key, rs.pathFolderData + "ThetaAllTraj/" + key)
            #remove(rs.pathFolderTrajectories + key)
    print(len(aa), aa)
    print(len(keyy), sorted(keyy))
        
    plt.figure()
    plt.scatter(x, y, c = "b", marker=u'o', s=25, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)  
    
    plt.show(block = True)
    

def plotPosTAT(fr, rs):
    xtr, junk = fr.recup_pos_ini(rs.pathFolderData + "ThetaAllTraj/")
    xt1, yt1 = [], []
    for key, el in xtr.items():
        xt1.append(el[0])
        yt1.append(el[1])
    plt.scatter(xt1, yt1, c = 'y')



#plot_pos_ini()
#Ce bout de code permet d'afficher les positions initiales des trajectoires dans output_solver(bin)
def plotPosIniOutputSolver():
    fr = FileReading()
    angleIni = {}
    Q = []
    name1 = "/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/"
    for el in os.listdir("/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/"):
        if "brentbvp" in el and not "fail" in el:
            #Chargement du fichier
            mati = np.loadtxt("/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/" + el)
            Q.append((el, mati[0,10], mati[0,11]))
            #recuperation de q1 et q2 initiales et conversion en coordonnees
            coordElbow, coordHand = mgd(np.mat([[mati[0,10]], [mati[0,11]]]), 0.3, 0.35)
            angleIni[el] = (coordHand[0], coordHand[1])
    
    angleIni2 = {}  
    name2 = "/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/cluster2/"
    for el in os.listdir("/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/cluster2/"):
        if "brentbvp" in el and not "fail" in el:
            #Chargement du fichier
            mati2 = np.loadtxt("/home/beucher/Desktop/Monfray/Codes/Java/bin/output_solver/cluster2/" + el)
            #Q.append((el, mati[0,10], mati[0,11]))
            #recuperation de q1 et q2 initiales et conversion en coordonnees
            coordElbow2, coordHand2 = mgd(np.mat([[mati2[0,10]], [mati2[0,11]]]), 0.3, 0.35)
            angleIni2[el] = (coordHand2[0], coordHand2[1])
    
    x, y, xy = [], [], []
    for key, el in angleIni.items():
        x.append(el[0])
        y.append(el[1])
        xy.append((key, el[0], el[1]))
        
    x2, y2, xy2 = [], [], []
    for key, el in angleIni2.items():
        x2.append(el[0])
        y2.append(el[1])
        xy2.append((key, el[0], el[1]))
    
    gt = []
    for el in xy2:
        if not el in xy:
            gt.append(el[0])
            #copyfile(name2 + el[0], name1 + el[0])
            
    print(len(gt), gt)
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(x2, y2, c = 'r')
    plt.show(block = True)
    
#plotPosIniOutputSolver()





