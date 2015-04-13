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
    fileSavingBin("trajectoires_cout/trajectoire_coutXBIN", valJuT)
    fileSavingStr("trajectoires_cout/nbiteX", Ite)
    print("Fin de traitement!")
    
        

    
    
    
    
    
    
