from math import sqrt
import numpy as np
from FileProcessing.FileReading import FileReading
from Regression.functionApproximator_LWR import fa_lwr
from ArmModel.ParametresArmModel import ParametresArmModel
from ArmModel.ParametresHogan import ParametresHogan
from ArmModel.ParametresRobot import ParametresRobot
from Regression.ControlerUtil import ControlerUtil
from ArmModel.SavingData import SavingData
from FileProcessing.FileSaving import fileSavingStr
from Regression.functionApproximator_RBFN2 import fa_rbfn

class costFunction:
    
    def __init__(self):
        self.gamma = 0.998
        self.rho = 10
        self.ups = 3000
        self.Ju = 0
        self.suivi = 0
        
    def costFunctionJ(self, U, action, t):
        usquare = np.square(U)
        usum = 0
        for el in usquare:
            usum += el
        mvtCost = (sqrt(usum))**2
        if action == 1:
            imReward = 0
        else:
            imReward = 1
        self.Ju += np.exp(-t/self.gamma)*(self.rho*imReward - self.ups*mvtCost)
        
    def costFunctionTest2(self, theta):
        nb = 0
        thetaTmp = {}
        for i in range(6):
            thetaTmp[i] = []
        for i in range(6):
            for j in range(int((theta.shape)[0]/6)):
                thetaTmp[i].append(theta[j + nb])
            nb += 81
        robot = ParametresRobot()
        hogan = ParametresHogan()
        arm = ParametresArmModel(hogan.GammaMax)
        save = SavingData()
        fr = FileReading()
        nbf = 3
        nbd = 4
        nbt = 0
        coordStartPts = []
        coordStartPts.append((-0.1,0.39))
        coordStartPts.append((0.0,0.39))
        coordStartPts.append((0.1,0.39))
        coordStartPts.append((0.2,0.39))
        coordStartPts.append((-0.2,0.0325))
        coordStartPts.append((-0.1,0.0325))
        coordStartPts.append((0.2,0.0325))
        coordStartPts.append((0.3,0.0325))
        JuCf = []
        xMinMax = fr.getxMinMax(nbf)
        fa = fa_lwr(nbf, nbd, 1, 2, xMinMax)
        #stateAll, commandAll = fr.recup_data(0)
        #fa = fa_rbfn(3)
        #fa.setTrainingData(stateAll.T, commandAll.T)
        #fa.setCentersAndWidths()
        cu = ControlerUtil(nbf,nbd)
        for el in coordStartPts:
            q1, q2 = fr.convertToAngle(el[0], el[1], robot)
            q = np.array([[q1],[q2]])
            dotq = np.array([[0.],[0.]])
            coordEL, coordHA = save.calculCoord(q, robot)
            i = 0
            arm.t = 0
            self.Ju = 0
            while coordHA[1] < 0.6175:
                if i < 900:
                    inputq = np.array([dotq[0,0], dotq[1,0], q[0,0], q[1,0]])
                    cu.getCommand(inputq, nbt, fa, thetaTmp, 1)
                    Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*cu.U
                    ddotq = arm.MDD( Gamma_AM,q,dotq,robot)
                    dotq += ddotq*arm.dt
                    q += dotq*arm.dt
                    coordEL, coordHA = save.calculCoord(q, robot)
                    if coordHA[0] == 0.0 and coordHA[1] == 0.6175:
                        self.costFunctionJ(cu.U, 2, arm.t)
                    else:
                        self.costFunctionJ(cu.U, 1, arm.t)
                else:
                    break
                i += 1
                arm.t += arm.dt
            print(i)
            JuCf.append(self.Ju*(-1))
        fileSavingStr("CalculCoutTest", JuCf)
        self.suivi += 1
        print("Fin d'appel! (", self.suivi, ")")
        return JuCf


fra2 = FileReading()
fra2.getTheta(3, 0)
thetaNorm = {}
thetaTmp = {}
cf = costFunction()
for i in range(6):
    thetaTmp[i] = []
for i in range(6):
    name = "ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)
    thetaNorm[i] = fra2.getobjread(name)
thetaN = np.array(thetaNorm[0])
thetann = np.array(fra2.theta_store["u1"])
for i in range(5):
    thetaN = np.hstack((thetaN, thetaNorm[i+1]))
    thetann = np.hstack((thetann, fra2.theta_store[str("u"+ str(i+2))]))
nb = 0
for i in range(6):
    for j in range(int((thetann.shape)[0]/6)):
        thetaTmp[i].append(thetann[j + nb])
    nb += 81
res = cf.costFunctionTest2(thetann)
print(res)




