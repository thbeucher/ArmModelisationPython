from FileProcessing.FileReading import FileReading
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
import numpy as np


def normalizeThetaFunction():
    fr = FileReading()
    fr.getTheta(3, 0)
    #Enregistrement des theta en Str
    for i in range(6):
        name = "ThetaAllTraj/Theta_u" + str(i+1)
        fileSavingStr(name, fr.theta_store[str("u" + str(i+1))])
    #Normalisation des theta
    for i in range(6):
        mini = np.min(fr.theta_store[str("u" + str(i+1))])
        maxi = np.max(fr.theta_store[str("u" + str(i+1))])
        v = fr.theta_store[str("u" + str(i+1))]
        v = (v - mini)/(maxi - mini)
        name = "ThetaAllTraj/thetaNormalize_u" + str(i+1)
        fileSavingStr(name, v)
        nameb = "ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)
        fileSavingBin(nameb, v)
    #Coefficient de normalisation
    for i in range(6):
        namec = "ThetaAllTraj/CoefNormalization_theta_u" + str(i+1)
        vTmp = fr.getobjread(str("ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)))
        coef = fr.theta_store[str("u" + str(i+1))][0] / vTmp[0]
        fileSavingBin(namec, coef)
    
    
normalizeThetaFunction()