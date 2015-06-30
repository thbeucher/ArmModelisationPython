'''
Author: Thomas Beucher

Module: NextStateComputation

Description: 
'''
import cma
import numpy as np
from Utils.InitUtil import initFRRS
from Regression.functionApproximator_RBFN import fa_rbfn
from testTGUKF.MuscularActivationCommandTGUKF import MuscularActivationCommand
from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters
from ArmModel.ArmDynamics import ArmDynamics
from testTGUKF.NextStateComputationTGUKF import NextStateComputation
from testTGUKF.UnscentedKalmanFilterControlTGUKF import UnscentedKalmanFilterControl
from testTGUKF.CostComputationTGUKF import CostComputation
from testTGUKF.TrajectoryGeneratorTGUKF import TrajectoryGenerator
from testTGUKF.TrajectoriesGeneratorTGUKF import TrajectoriesGenerator
from Utils.ThetaNormalization import normalizationNP, matrixToVector

import matplotlib.pyplot as plt

def initController(rs, fr):
    fa = fa_rbfn(rs.numfeats)
    state, command = fr.getData(rs.pathFolderTrajectories)
    stateAll, commandAll = fr.dicToArray(state), fr.dicToArray(command)
    fa.setTrainingData(stateAll.T, commandAll.T)
    fa.setCentersAndWidths()
    return fa

def initAllUsefullObj(sizeOfTarget, fr, rs):
    fa = initController(rs, fr)
    mac = MuscularActivationCommand()
    mac.initParametersMAC(fa, rs)
    armP = ArmParameters()
    musclesP = MusclesParameters()
    armD = ArmDynamics()
    nsc = NextStateComputation()
    nsc.initParametersNSC(mac, armP, rs, musclesP)
    Ukf = UnscentedKalmanFilterControl()
    Ukf.initParametersUKF(4, 2, 25, nsc)
    cc = CostComputation()
    cc.initParametersCC(rs)
    tg = TrajectoryGenerator()
    tg.initParametersTG(armP, rs, nsc, cc, sizeOfTarget, Ukf, armD)
    tgs = TrajectoriesGenerator()
    tgs.initParametersTGS(rs, 5, tg, 4, 6, mac)
    return tgs

def launchCMAESForSpecificTargetSize(sizeOfTarget):
    print("Start of the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    fr, rs = initFRRS()
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    theta = normalizationNP(theta, rs)
    theta = matrixToVector(theta)
    tgs = initAllUsefullObj(sizeOfTarget, fr, rs)
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, theta, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    nameToSaveThetaCma = rs.pathFolderData + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/thetaCma" + str(sizeOfTarget) + "opti1"
    np.savetxt(nameToSaveThetaCma, resCma[0])
    print("End of optimization for target " + str(sizeOfTarget) + " !")
    
    
    
    
def testNewKalman():
    fr, rs = initFRRS()
    tgs = initAllUsefullObj(rs.sizeOfTarget[3], fr, rs)
    x, y = 0.1, 0.35
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    tgs.mac.setThetaMAC(theta)
    cost = tgs.tg.runTrajectory(x, y)
    print("cost: ", cost)
    print(tgs.tg.SaveCoordWK, "\n", tgs.tg.SaveCoordUKF)
    for key, val in tgs.tg.SaveCoordWK.items():
        WK = [el for el in val]
        UKF = [el for el in tgs.tg.SaveCoordUKF[key]]
    print(WK)
    difTab = []
    for el1, el2 in zip(WK, UKF):
        a = np.sqrt((el1[0] - el2[0])**2 + (el1[1] - el2[1])**2)
        difTab.append(a)
    t = [i for i in range(len(difTab))]
    plt.figure()
    plt.plot([x[0] for x in WK], [y[1] for y in WK], c = 'b')
    plt.plot([x[0] for x in UKF], [y[1] for y in UKF], c = 'r')
    plt.figure()
    plt.plot(t, difTab)
    plt.show(block = True)
        
        
#testNewKalman()
    
    
    
    
    