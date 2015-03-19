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

class costFunction:
    
    def __init__(self):
        self.gamma = 0.998
        self.rho = 10
        self.ups = 3000
        self.Ju = 0
        
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


def costFunctionTest(theta):
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
    for el in coordStartPts:
        cf = costFunction()
        cu = ControlerUtil(nbf,nbd)
        q1, q2 = fr.convertToAngle(el[0], el[1], robot)
        q = np.mat([[q1],[q2]])
        dotq = np.mat([[0.],[0.]])
        coordEL, coordHA = save.calculCoord(q, robot)
        i = 0
        arm.t = 0
        while coordHA[1] < 0.6175:
            if i < 900:
                inputq = np.array([dotq[0,0], dotq[1,0], q[0,0], q[1,0]])
                cu.getCommand(inputq, nbt, theta, 1)
                Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*cu.U
                ddotq = arm.MDD( Gamma_AM,q,dotq,robot)
                dotq += ddotq*arm.dt
                q += dotq*arm.dt
                coordEL, coordHA = save.calculCoord(q, robot)
                if coordHA[0] == 0.0 and coordHA[1] == 0.6175:
                    cf.costFunctionJ(cu.U, 2, arm.t)
                else:
                    cf.costFunctionJ(cu.U, 1, arm.t)
            else:
                break
            i += 1
            arm.t += arm.dt
        print(i)
        JuCf.append(cf.Ju)
        cf.Ju = 0
    fileSavingStr("CalculCoutTest", JuCf)
    return JuCf

'''fra2 = FileReading()
fra2.getTheta(3, 0)
res = costFunctionTest(fra2.theta_store)
print(res)'''








