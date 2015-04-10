'''
Author: Thomas Beucher

Module: RunTrajectories

Description: Ce fichier contient les fonctions permettant de lancer la generation des trajectoires
'''
from Utils.FileReading import FileReading
from Optimisation.costFunction import costFunction
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
    

def runGenTraj():
    ##code permettant de lancer la fonction de generation de trajectoire
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    noise = input("Avec bruit moteur? (Y or N): ")
    print("(0: Rien / 1: U / 2: Unoise / 3: CoordTrajU / 4: CoordTrajUnoise / 5: nbIte")
    sauv = input("Que voulez vous sauvegarder?: ")
    sauv = int(sauv)
    fra = FileReading()
    nbtra = input("Sur combien de trajectoire voulez vous le theta(12 ou X): ")
    if nbtra == "12":
        name = "RBFN2/" + str(nbfeat) + "feats/ThetaBIN"
        names = "RBFN2/" + str(nbfeat) + "feats/cout"
        namesb = "RBFN2/" + str(nbfeat) + "feats/coutBIN"
        if noise == "Y":
            cf = costFunction(nbfeat, 1, 1, sauv)
        elif noise == "N":
            cf = costFunction(nbfeat, 1, 0, sauv)
    elif nbtra == "X":
        name = "RBFN2/" + str(nbfeat) + "feats/ThetaXBIN"
        if noise == "Y":
            names = "RBFN2/" + str(nbfeat) + "feats/coutNoiseX"
            names2 = "RBFN2/" + str(nbfeat) + "feats/coutNoiseXBIN"
            cf = costFunction(nbfeat, 0, 1, sauv)    
        elif noise == "N":
            names = "RBFN2/" + str(nbfeat) + "feats/coutX"
            names2 = "RBFN2/" + str(nbfeat) + "feats/coutXBIN"
            cf = costFunction(nbfeat, 0, 0, sauv)
    theta = fra.getobjread(name)
    res = cf.costFunctionRBFN2(theta)
    testju = cf.costFunctionRBFN2Test(theta)#TEST
    print(testju)#TEST
    print(res)
    fileSavingStr(names, res)
    fileSavingBin(names2, res)
    
    
def runGenTrajCma():
    ##code permettant de lancer la fonction de generation de trajectoire
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    noise = input("Avec bruit moteur? (Y or N): ")
    print("(0: Rien / 1: U / 2: Unoise / 3: CoordTrajU / 4: CoordTrajUnoise / 5: nbIte")
    sauv = input("Que voulez vous sauvegarder?: ")
    sauv = int(sauv)
    fra = FileReading()
    name = "OptimisationResults/thetaSolBIN"
    if noise == "Y":
        names = "RBFN2/" + str(nbfeat) + "feats/coutNoiseCmaX"
        names2 = "RBFN2/" + str(nbfeat) + "feats/coutNoiseXCmaBIN"
        cf = costFunction(nbfeat, 0, 1, sauv)
    elif noise == "N":
        names = "RBFN2/" + str(nbfeat) + "feats/coutXCma"
        names2 = "RBFN2/" + str(nbfeat) + "feats/coutXCmaBIN"
        cf = costFunction(nbfeat, 0, 0, sauv)
    theta = fra.getobjread(name)
    maxT = fra.getobjread("OptimisationResults/maxTBIN")
    theta = theta*maxT
    nb = 0
    for i in range(int(theta.shape[0]/6)):
        thetaTmp = []
        for j in range(6):
            thetaTmp.append(theta[j + nb])
        if i == 0:
            thetaf = np.array([thetaTmp])
        else:
            thetaf = np.vstack((thetaf, np.array([thetaTmp])))
        nb += 6
    theta = thetaf
    res = cf.costFunctionRBFN2(theta, 1)
    print(res)
    fileSavingStr(names, res)
    fileSavingBin(names2, res)