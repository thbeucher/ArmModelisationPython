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
    
    plt.show(block = True)
    




'''fr = FileReading()
rs = ReadSetupFile()
traj, junk = fr.recup_pos_ini(rs.pathFolderData + "ThetaAllTraj/")
trajx, trajy, tx, ty, k, ksupr = [], [], [], [], [], []
for key1, el1 in traj.items():
    trajx.append(el1[0])
    trajy.append(el1[1])
    for key2, el2 in traj.items():
        a = abs(el1[0] - el2[0])
        b = abs(el1[1] - el2[1])
        if el1[0] == el2[0] and el1[1] == el2[1] and key2 != key1:
            print("la", key1, key2)
        if a < 0.008 and b < 0.008 and key2 != key1:
            if key1 not in k:
                print("ic", key1, key2)
                k.append(key1)
                k.append(key2)
                tx.append(el2[0])
                ty.append(el2[1])
                ksupr.append(key1)
#for el in ksupr:
    #remove(rs.pathFolderData + "ThetaAllTraj/" + el)

plt.figure()
plt.scatter(trajx, trajy, c = 'b')
plt.scatter(tx, ty, c = 'r')
plt.show()'''
    
    
    



