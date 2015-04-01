'''
Author: Thomas Beucher
Module: Functions
'''
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from ArmModel.SavingData import SavingData
from FileProcessing.FileReading import FileReading





def normalizeThetaFunction():
    fr = FileReading()
    fr.getTheta(3, 0)
    vzeros = []
    #Enregistrement des theta en Str
    for i in range(6):
        name = "ThetaAllTraj/Theta_u" + str(i+1)
        fileSavingStr(name, fr.theta_store[str("u" + str(i+1))])
    #Normalisation des theta
    for i in range(6):
        mini = np.min(fr.theta_store[str("u" + str(i+1))])
        maxi = np.max(fr.theta_store[str("u" + str(i+1))])
        vs = fr.theta_store[str("u" + str(i+1))]
        v = (vs - mini)/(maxi - mini)
        vtest = v + 0.1
        name = "ThetaAllTraj/thetaNormalize_u" + str(i+1)
        fileSavingStr(name, v)
        nameb = "ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)
        fileSavingBin(nameb, v)
    #Coefficient de normalisation
    for i in range(6):
        namec = "ThetaAllTraj/CoefNormalization_theta_u" + str(i+1)
        vTmp = fr.getobjread(str("ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)))
        coef =  np.divide(vTmp, fr.theta_store[str("u" + str(i+1))])
        fileSavingBin(namec, coef)
        fileSavingStr(str(namec + "_str"), coef)

    
    
'''normalizeThetaFunction()
f = FileReading()
for i in range(6):
    tn = f.getobjread(str("ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)))
    coef = f.getobjread(str("ThetaAllTraj/CoefNormalization_theta_u" + str(i+1)))
    tl = np.divide(tn, coef)
    fileSavingStr(str("ThetaAllTraj/thetaRetrouve_u" + str(i+1)), tl)'''











