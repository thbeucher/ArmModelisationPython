'''
Author: Thomas Beucher

Module: plotFunctions

Description: On retrouve dans ce fichier differentes fonctions permettant d'afficher les resultats du projet
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from Utils.FileReading import FileReading
from matplotlib import animation
from matplotlib.mlab import griddata
import mpl_toolkits
from Utils.ReadSetupFile import ReadSetupFile
import os


def costColorPlot(wha):
    '''
    Cette fonction permet d'afficher le profil de cout des trajectoires
    
    Entrees:    -nbfeat: nombre de features utilises pour generer le controleur actuel
                -wha: choix des donnees a afficher
    '''
    xt = 0
    
    fr = FileReading()
    rs = ReadSetupFile()
    nbfeat = rs.numfeats
    
    xy0tmp, Q = fr.recup_pos_ini(rs.pathFolderTrajectories)
    x0 = []
    y0 = []
    posi = fr.getobjread(rs.experimentFilePosIni)
    for el in posi:
        x0.append(el[0])
        y0.append(el[1])
        
    if wha == "rbfn":
        name = "RBFN2/" + str(nbfeat) + "feats/costBIN"
        z = fr.getobjread(name)
        for i in range(len(z)):
            if z[i] > 50:
                z[i] -= 3000
        maxt = np.max(abs(z))
        
    elif wha == "cma":
        name = "RBFN2/" + str(nbfeat) + "feats/costBINCma"
        z = fr.getobjread(name)
        maxt = np.max(abs(z))
        
    elif wha == "brent":
        z = fr.getobjread("trajectoires_cout/trajectoire_coutXBIN")
        z = np.array(z)
        z = z-3000
        maxt = np.max(abs(z))
        x0 = []
        y0 = []
        for el in xy0tmp.values():
            x0.append(el[0])
            y0.append(el[1])
    
    zb = z/maxt
    xi = np.linspace(-0.4,0.4,280)
    yi = np.linspace(0.1,0.6,280)
    zi = griddata(x0, y0, zb.T[0], xi, yi)
    
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=zb, marker=u'o', s=200, cmap=cm.get_cmap('RdYlBu'))
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
    fr = FileReading()
    rs = ReadSetupFile()
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
    

def plot_pos_ini():
    '''
    Cette fonction permet d'afficher les positions initiales des trajectoires
    (trajectoire disponible dans le dossier trajectoire)           
    '''
    x0 = []
    y0 = []
    fr = FileReading()
    rs = ReadSetupFile()
    xt = 0
    yt = rs.targetOrdinate
    posIni = fr.getobjread(rs.experimentFilePosIni)
    for el in posIni:
        x0.append(el[0])
        y0.append(el[1])
    xy, junk = fr.recup_pos_ini(rs.pathFolderTrajectories)
    x, y = [], []
    for el in xy.values():
        x.append(el[0])
        y.append(el[1])
        
    plt.figure()
    plt.scatter(x, y, c = "b", marker=u'o', s=25, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)  
    
    plotPosTAT(fr, rs)
    
    plt.show(block = True)
    

def plotPosTAT(fr, rs):
    xtr, junk = fr.recup_pos_ini(rs.pathFolderData + "ThetaAllTraj/")
    xt1, yt1 = [], []
    for el in xtr.values():
        xt1.append(el[0])
        yt1.append(el[1])
    plt.scatter(xt1, yt1, c = 'y')


    
    
    



