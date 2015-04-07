from Optimisation.costFunction import costFunction
from Utils.FileReading import FileReading
from Utils.FileSaving import fileSavingStr, fileSavingBin
import os
import numpy as np
from ArmModel.SavingData import SavingData
from ArmModel.ParametresRobot import ParametresRobot

def costEvalBrent():
    print("Debut de traitement!")
    cf = costFunction(3)
    save = SavingData()
    robot = ParametresRobot()
    save = SavingData()
    #Chargement des donnees de trajectoire
    fileR = FileReading()
    stateAll, commandAll = fileR.recup_data(1)
    a = 0
    nbj = []
    nameX = "trajectoires_cout/trajectoire_coutX"
    nameXBIN = "trajectoires_cout/trajectoire_coutXBIN"
    nameite = "trajectoires_cout/nbiteX"
    trajC = []
    for i in range(int(len(fileR.data_store)/2)):
        if not str("trajectoire" + str(i+1+a) + "_command") in fileR.data_store:
            a += 1
        nbj.append(len(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")]))
        for j in range(len(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")])):
            el = fileR.data_store[str("trajectoire" + str(i+1+a) + "_state")][j]
            q = np.array([[el[2]], [el[3]]])
            coordEL, coordHA = save.calculCoord(q, robot)
            if(coordHA[0] == 0 and coordHA[1] == 0.6175):
                cf.costFunctionJ(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")][j], 1, 0.002)
            else:
                cf.costFunctionJ(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")][j], 0, 0.002)
        #q = np.mat([[(fileR.data_store[str("trajectoire" + str(i+1+a) + "_state")][j+1])[2]],[(fileR.data_store[str("trajectoire" + str(i+1+a) + "_state")][j+1])[3]]])
        #coordEL, coordHA = save.calculCoord(q, robot)
        #print("coordHa: ", coordHA)
        #c = input("cocuou")
        name = "trajectoires_cout/trajectoire" + str(i+1+a) + "_cout"
        trajC.append(cf.Ju)
        cf.Ju = 0
    fileSavingStr(nameX, trajC)
    fileSavingBin(nameXBIN, trajC)
    fileSavingStr(nameite, nbj)
    print("Fin de traitement!")
