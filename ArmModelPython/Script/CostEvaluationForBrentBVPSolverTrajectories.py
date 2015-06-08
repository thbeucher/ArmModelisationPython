from Utils.FileReading import FileReading
from Utils.FileSaving import fileSavingStr, fileSavingBin
import os
import numpy as np
from ArmModel.GeometricModel import mgd
from Utils.ReadSetupFile import ReadSetupFile
from ArmModel.ArmParameters import ArmParameters
from Main.GenerateTrajectory import GenerateTrajectory
from Utils.NiemRoot import tronquerNB
    

#####################################
#             OutDated              #
#####################################
def costEvalBrent():
    print("Debut de traitement!")
    sti = GenerateTrajectory()
    stateAll, commandAll = sti.fr.getData(sti.rs.pathFolderTrajectories)
    JuT, JuWR = {}, {}
    Ite = []
    valJuT = []
    JuT2 = []
    for el in commandAll:
        t, Ju = 0, 0
        u = np.array(commandAll[el])
        Ite.append(u.shape[0])
        for i in range(u.shape[0]):
            Ju = sti.costComputation(Ju, u[i], t)
            t += sti.rs.dt
        coordEl, coordHa = mgd(np.array([[stateAll[el][u.shape[0]-1][2]], [stateAll[el][u.shape[0]-1][3]]]), sti.armP.l1, sti.armP.l2)
        JuWR[el] = Ju
        if((coordHa[0] >= (0-sti.targetSizeS/2) and coordHa[0] <= (0+sti.targetSizeS/2)) and coordHa[1] >= (sti.rs.targetOrdinate - sti.rs.errorPosEnd)):
            Ju += np.exp(-t/sti.rs.gammaCF)*sti.rs.rhoCF
        JuT[el] = Ju
        valJuT.append(Ju)
        junk, coordInitHA = mgd(np.array([[stateAll[el][0][2]], [stateAll[el][0][3]]]), sti.armP.l1, sti.armP.l2)
        elname = str(str(round(coordInitHA[0], 4)) + "//" + str(round(coordInitHA[1], 4)))
        JuWR[elname] = JuWR[el]
        del JuWR[el]
        JuT2.append((el, Ju, tronquerNB(coordInitHA[0], 5), tronquerNB(coordInitHA[1], 5)))
    print(JuT)
    print(JuT2)
    fileSavingBin("trajectoires_cout/trajectoire_coutCoordXBIN", JuT2)
    fileSavingStr("trajectoires_cout/trajectoire_coutX", JuT.items())
    fileSavingBin("trajectoires_cout/trajectoire_coutXBIN", JuT)
    fileSavingStr("trajectoires_cout/nbiteX", Ite)
    fileSavingBin("trajectoires_cout/actiMuscuBIN", JuWR)
    fileSavingStr("trajectoires_cout/actiMuscu", JuWR)
    print("Fin de traitement!")
    
        
#costEvalBrent()
    
    
    
    
    
    
