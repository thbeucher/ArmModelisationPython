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
from os.path import isfile
from shutil import copyfile
from posix import remove


def costColorPlot(wha):
    '''
    Cette fonction permet d'afficher le profil de cout des trajectoires
    
    Entrees:    -nbfeat: nombre de features utilises pour generer le controleur actuel
                -wha: choix des donnees a afficher
    '''
    xt = 0
    yt = 0.6175
    x0 = [-0.2,-0.1,0,0.1,0.2,-0.3,-0.2,-0.1,0,0.1,0.2,0.3]
    y0 = [0.39,0.39,0.39,0.39,0.39,0.26,0.26,0.26,0.26,0.26,0.26,0.26]
    
    fr = FileReading()
    rs = ReadSetupFile()
    nbfeat = rs.numfeats
    
    xy0tmp, Q = fr.recup_pos_ini(rs.pathFolderTrajectories)
    x0 = []
    y0 = []
        
    if wha == "rbfn":
        name = "RBFN2/" + str(nbfeat) + "feats/costBIN"
        z = fr.getobjread(name)
        ztmp = []
        zkey = []
        for el in z:
            if el[1] > 2500:
                ztmp.append(el[1])
                zkey.append(el[0])
        xyTmp = []
        for el in zkey:
            if el in xy0tmp.keys():
                xyTmp.append(xy0tmp[el])
        for el in xyTmp:
            x0.append(el[0])
            y0.append(el[1])
        z = np.array(ztmp)
        z = z - 3000
        maxt = np.max(abs(z))
        
    elif wha == "cma":
        pass
    elif wha == "brent":
        z = fr.getobjread("trajectoires_cout/trajectoire_coutXBIN")
        z = np.array(z)
        z = z-3000
        maxt = np.max(abs(z))
        for el in xy0tmp.values():
            x0.append(el[0])
            y0.append(el[1])
        
    zb = z/maxt
    xi = np.linspace(-0.4,0.4,100)
    yi = np.linspace(0.1,0.5,100)
    zi = griddata(x0, y0, zb, xi, yi)
    
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=zb, marker=u'o', s=200, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c ='g', marker='v', s=200)
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
        '''ch = input("Voulez vous afficher les activations musculaires avec bruit?(Y or N): ")
        trajIteU = {}
        trajVal = {}
        for i in range(6*12):
            trajVal[i] = []
        u = 0
        for i in range(12):
            trajIteU[i] = []
            if ch == "N":
                nameU = "RBFN2/" + str(nbfeat) + "feats/MuscularActivation/ActiMuscuTrajectoireXCma" + str(i+1)
            elif ch == "Y":
                nameU = "RBFN2/" + str(nbfeat) + "feats/MuscularActivation/ActiMuscuNoiseTrajectoireXCma" + str(i+1)
            ut1 = fr.getobjread(nameU)
            for j in range(len(ut1)):
                trajIteU[i].append(j)
                for t in range(6):
                    trajVal[t+u].append(ut1[j][t])
            u += 6
        u = 0
        for i in range(12):
            rbfn = plt.Figure()
            for j in range(6):
                plt.plot(trajIteU[i], trajVal[j+u])
            u += 6
            plt.show(block = True)'''
    

def plot_pos_ini():
    '''
    Cette fonction permet d'afficher les positions initiales des trajectoires
    (trajectoire disponible dans le dossier trajectoire)           
    '''
    xt = 0
    yt = 0.6175
    x0 = [-0.2,-0.1,0,0.1,0.2,-0.3,-0.2,-0.1,0,0.1,0.2,0.3]
    y0 = [0.39,0.39,0.39,0.39,0.39,0.26,0.26,0.26,0.26,0.26,0.26,0.26]
    fr = FileReading()
    rs = ReadSetupFile()
    rs.readingSetupFile()
    patht = rs.pathFolderTrajectories
    xy, junk = fr.recup_pos_ini(patht)
    x, y = [], []
    for el in xy.values():
        x.append(el[0])
        y.append(el[1])
        
    '''
    #verifie si les trajectoires d'entrainement comprenne les trajectoires d'experimentation
    a = 0
    for el in xy:
        for i in range(len(x0)):
            if el[0] == x0[i] and el[1] == y0[i]:
                a += 1
    print(a)'''
    '''xyt = fr.recup_pos_ini("/home/beucher/workspace/recupTraj/")
    xtt, ytt = [], []
    for el in xyt.values():
        xtt.append(el[0])
        ytt.append(el[1])'''
        
    plt.figure()
    plt.scatter(x, y, c = "b", marker=u'o', s=25, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c = "r", marker=u'*', s = 100)
    plt.scatter(x0, y0, c = "r", marker=u'o', s=25)  
    
    #plt.scatter(xtt, ytt, c = 'y')
    
    plt.show(block = True)
    

    
                







