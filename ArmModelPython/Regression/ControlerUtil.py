from Regression.functionApproximator_LWR import fa_lwr
from FileProcessing.FileReading import FileReading
import numpy as np

class ControlerUtil:
    def __init__(self, nbfeature, dime):
        self.nbfeat = nbfeature
        self.dim = dime
        self.faOutStore = {}
        
    def getCommand(self, inputgc, numTrajectoire, theta, a = 0):
        fr = FileReading()
        thetaTmp = {}
        for i in range(6):
            thetaTmp[i] = []
        xMinMax = fr.getxMinMax(self.nbfeat)
        fa = fa_lwr(self.nbfeat, self.dim, 1, 2, xMinMax)
        #Recuperation des thetas pour chaque u (activations musculaires)
        if a == 0:
            fr.getTheta(self.nbfeat, numTrajectoire)
        else:
            for i in range(6):
                coef = fr.getobjread(str("ThetaAllTraj/CoefNormalization_theta_u" + str(i+1)))
                for j in range(int((theta.shape)[0]/6)):
                    thetaTmp[i].append(theta[j]*coef)
        #Recuperation de la sortie approximee pour chaque u
        for i in range(6):
            if a == 0:
                self.faOutStore[str("faOut_u" + str(i+1))] = fa.functionApproximatorOutputLS(inputgc, fr.theta_store[str("u" + str(i+1))], 2)
            else:
                self.faOutStore[str("faOut_u" + str(i+1))] = fa.functionApproximatorOutputLS(inputgc, thetaTmp[i], 2)
        #Mise sous forme de vecteur
        self.U = np.zeros((6,1))
        for i in range(6):
            self.U[i,0] = self.faOutStore[str("faOut_u" + str(i+1))]
        
        