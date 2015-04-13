'''
Author: Thomas Beucher

Module: RunTrajectories

Description: Ce fichier contient les fonctions permettant de lancer la generation des trajectoires
'''
from Utils.FileReading import FileReading
from Utils.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from Utils.ReadSetupFile import ReadSetupFile
from Optimisation.costFunction import costFunctionRBFN
    
    
def runGenTraj():
    fr = FileReading()
    rs = ReadSetupFile()
    print("(0: nothing / 1: CoordTraj / 2: U / 3: nbIte, 4: cost)")
    sauv = input("voulez vous sauvegarder les trajectoires: ")
    sauv = int(sauv)
    nameT = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread(nameT + "ThetaXBIN")
    testju, sti = costFunctionRBFN(theta)
    if sauv == 1:
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireELAll", sti.save.coordElSave)
        fileSavingBin(nameT + "CoordTraj/CoordTrajectoireHAAll", sti.save.coordHaSave)
    elif sauv == 2:
        fileSavingBin(nameT + "Uall", sti.Usave)
    elif sauv == 3:
        fileSavingStr(nameT + "nbIte", sti.IteSave)
    elif sauv == 4:
        fileSavingStr(nameT + "cost", testju)
        fileSavingBin(nameT + "costBIN", testju)
    print(testju)  
    
    
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
        #cf = costFunction(nbfeat, 0, 1, sauv)
    elif noise == "N":
        names = "RBFN2/" + str(nbfeat) + "feats/coutXCma"
        names2 = "RBFN2/" + str(nbfeat) + "feats/coutXCmaBIN"
        #cf = costFunction(nbfeat, 0, 0, sauv)
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
    #res = cf.costFunctionRBFN2(theta, 1)
    #print(res)
    #fileSavingStr(names, res)
    #fileSavingBin(names2, res)