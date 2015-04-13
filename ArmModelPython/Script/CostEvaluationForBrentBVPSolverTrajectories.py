from Optimisation.costFunction import costFunction
from Utils.FileReading import FileReading
from Utils.FileSaving import fileSavingStr, fileSavingBin
import os
import numpy as np
from ArmModel.GeometricModel import mgd
from Utils.ReadSetupFile import ReadSetupFile
from ArmModel.ArmParameters import ArmParameters
from Main.SuperToolsInit import SuperToolsInit

def costEvalBrent():
    print("Debut de traitement!")
    cf = costFunction(3)
    rs = ReadSetupFile()
    armP = ArmParameters()
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
        stopite = 0
        for j in range(len(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")])):
            el = fileR.data_store[str("trajectoire" + str(i+1+a) + "_state")][j]
            q = np.array([[el[2]], [el[3]]])
            coordEL, coordHA = mgd(q, armP.l1, armP.l2)
            if((coordHA[0] >= (0-rs.sizeOfTarget/2) and coordHA[0] <= (0+rs.sizeOfTarget/2)) and coordHA[1] >= rs.targetOrdinate):
                if stopite == 0:
                    stopite += 1
                    cf.costFunctionJ(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")][j], 2, 0.002)
            else:
                cf.costFunctionJ(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")][j], 1, 0.002)
        trajC.append(cf.Ju)
        cf.Ju = 0
    fileSavingStr(nameX, trajC)
    fileSavingBin(nameXBIN, trajC)
    fileSavingStr(nameite, nbj)
    print("Fin de traitement!")
    
    
    
    
def costEvalBrent2():
    sti = SuperToolsInit()
    stateAll, commandAll = sti.fr.getData()
    JuT = {}
    Ite = []
    valJuT = []
    for el in commandAll:
        t, Ju = 0, 0
        u = np.array(commandAll[el])
        Ite.append(u.shape[0])
        for i in range(u.shape[0]):
            Ju = sti.costFunction(Ju, u[i], t)
            t += sti.rs.dt
        coordEl, coordHa = mgd(np.array([[stateAll[el][u.shape[0]-1][2]], [stateAll[el][u.shape[0]-1][3]]]), sti.armP.l1, sti.armP.l2)
        if coordHa[0] >= (0-sti.rs.sizeOfTarget/2) and coordHa[0] <= (0+sti.rs.sizeOfTarget/2) and coordHa[1] >= (sti.rs.targetOrdinate - 0.0001):
            Ju += sti.rs.rhoCF
        JuT[el] = Ju
        valJuT.append(Ju)
    print(JuT)
    fileSavingStr("trajectoires_cout/trajectoire_coutX", JuT.items())
    fileSavingBin("trajectoires_cout/trajectoire_coutXBINtest", valJuT)
    fileSavingStr("trajectoires_cout/nbiteX", Ite)
    
        

    
    
    
    
    
    
