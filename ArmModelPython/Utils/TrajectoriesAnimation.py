'''
Author: Thomas Beucher

Module: Animation

Description: On retrouve dans ce fichier le script permettant de lancer l'animation des trajectoires realisees
'''

from ArmModel.SavingData import SavingData
import matplotlib.pyplot as plt
from matplotlib import animation
from Utils.FileReading import FileReading
from Utils.ReadSetupFile import ReadSetupFile


def trajectoriesAnimation():
    choix = input("Veuillez choisir la trajectoire a visualiser(All or AllNoise or AllNoiseCma): ")
    fr = FileReading()
    save = SavingData()
    rs = ReadSetupFile()
    nbfeat = rs.numfeats
    #Recuperation des positions initiales
    posIni = fr.getobjread(rs.experimentFilePosIni)
    xIni, yIni = [], []
    for el in posIni:
        xIni.append(el[0])
        yIni.append(el[1])
    
    fig = plt.figure()
    upperArm, = plt.plot([],[]) 
    foreArm, = plt.plot([],[])
    plt.xlim(-0.7, 0.7)
    plt.ylim(-0.7,0.7)
    plt.plot([-0.7,0.7], [0.6175, 0.6175])
    plt.scatter([0-rs.sizeOfTarget/2, 0+rs.sizeOfTarget/2], [rs.targetOrdinate, rs.targetOrdinate], c ='g', marker='o', s=50)
    plt.scatter(xIni,yIni, c='b')
    
    
    #Fonction d'initialisation pour l'animation
    def init():
        upperArm.set_data([0],[0])
        foreArm.set_data([save.xEl[0]],[save.yEl[0]])
        return upperArm,foreArm,
    
    #Fonction utiliser pour generer les differentes position du bras pour l'animation     
    def animate(i): 
        xe = (0, save.xEl[i])
        ye = (0, save.yEl[i])
        xh = (save.xEl[i], save.xHa[i])
        yh = (save.yEl[i], save.yHa[i])
        upperArm.set_data(xe, ye)
        foreArm.set_data(xh, yh)
        return upperArm,foreArm
    
    if choix == "All":
        nameCoordEL = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireEL" + choix
        nameCoordHA = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireHA" + choix
        coordEL = fr.getobjread(nameCoordEL)
        coordHA = fr.getobjread(nameCoordHA)
        save.createCoord(2, coordHA, coordEL)
        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
        plt.show(block = True)
    elif choix == "AllNoise":
        nameCoordEL = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireEL" + choix
        nameCoordHA = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireHA" + choix
        coordEL = fr.getobjread(nameCoordEL)
        coordHA = fr.getobjread(nameCoordHA)
        save.createCoord(2, coordHA, coordEL)
        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
        plt.show(block = True)
    elif choix == "AllNoiseCma":
        nameCoordEL = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireEL" + choix
        nameCoordHA = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireHA" + choix
        coordEL = fr.getobjread(nameCoordEL)
        coordHA = fr.getobjread(nameCoordHA)
        save.createCoord(2, coordHA, coordEL)
        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
        plt.show(block = True)
    else: 
        nameCoordEL = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireEL" + choix
        nameCoordHA = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireHA" + choix
        coordEL = fr.getobjread(nameCoordEL)
        coordHA = fr.getobjread(nameCoordHA)
        save.createCoord(2, coordHA, coordEL)
        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
        plt.show()
        
        
        

        
