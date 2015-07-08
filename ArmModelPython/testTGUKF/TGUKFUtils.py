'''
Author: Thomas Beucher

Module: NextStateComputation

Description: 
'''
import cma
import numpy as np
from multiprocessing.pool import Pool
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
from Utils.FileSaving import fileSavingBin, fileSavingStr

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
    armD.initParametersAD(armP, musclesP, rs.dt)
    nsc = NextStateComputation()
    nsc.initParametersNSC(mac, armP, rs, musclesP)
    Ukf = UnscentedKalmanFilterControl()
    Ukf.initParametersUKF(6, 4, 15, nsc, armD, mac)
    cc = CostComputation()
    cc.initParametersCC(rs)
    tg = TrajectoryGenerator()
    tg.initParametersTG(armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac)
    tgs = TrajectoriesGenerator()
    tgs.initParametersTGS(rs, 5, tg, 4, 6, mac)
    return tgs

def fileSavingData(nameFile, data):
    fileSavingStr(nameFile, data)
    nameFile = nameFile + "BIN"
    fileSavingBin(nameFile, data)

def fileSavingAllData(sizeOfTarget, tg):
    nameSave = "OptimisationResults/ResCma" + str(sizeOfTarget) + "/ResUKF1B/"
    fileSavingData(nameSave + "saveNumberOfIteration", tg.saveNumberOfIteration)
    fileSavingData(nameSave + "saveCoordEndTraj", tg.saveCoordEndTraj)
    fileSavingData(nameSave + "saveMvtCost", tg.saveMvtCost)
    fileSavingData(nameSave + "saveSpeed", tg.saveSpeed)
    
def generateResults():
    fr, rs = initFRRS()
    for el in rs.sizeOfTarget:
        print("Results generation for target ", el)
        thetaName = rs.pathFolderData + "OptimisationResults/ResCma" + str(el) + "/thetaCma" + str(el) + "TGUKF1"
        theta = np.loadtxt(thetaName)
        tgs = initAllUsefullObj(el, fr, rs)
        tgs.runTrajectoriesResultsGeneration(theta, 30)
        fileSavingAllData(el, tgs.tg)
    print("End of generation")
    
#generateResults()

def launchCMAESForSpecificTargetSize(sizeOfTarget):
    print("Start of the CMAES Optimization for target " + str(sizeOfTarget) + " !")
    fr, rs = initFRRS()
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    theta = normalizationNP(theta, rs)
    theta = matrixToVector(theta)
    tgs = initAllUsefullObj(sizeOfTarget, fr, rs)
    resCma = cma.fmin(tgs.runTrajectoriesCMAWithoutParallelization, theta, rs.sigmaCmaes, options={'maxiter':rs.maxIterCmaes, 'popsize':rs.popsizeCmaes})
    nameToSaveThetaCma = rs.pathFolderData + "OptimisationResults/ResCma" + str(sizeOfTarget) + "/thetaCma" + str(sizeOfTarget) + "TGUKF1"
    np.savetxt(nameToSaveThetaCma, resCma[0])
    print("End of optimization for target " + str(sizeOfTarget) + " !")
    
def launchCMAESForAllTargetSize():
    fr, rs =initFRRS()
    p = Pool(4)
    p.map(launchCMAESForSpecificTargetSize, rs.sizeOfTarget)

#launchCMAESForAllTargetSize()



def testLastKalman():
    fr, rs = initFRRS()
    tgs = initAllUsefullObj(rs.sizeOfTarget[3], fr, rs)
    x, y = 0.1, 0.35
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    tgs.mac.setThetaMAC(theta)
    cost = tgs.tg.runTrajectory(x, y)
    for val in tgs.tg.SaveCoordWK.values():
        coordXY = val
    plt.figure()
    plt.plot([x[0] for x in coordXY], [y[1] for y in coordXY])
    plt.show(block = True)

#testLastKalman()
    
def testNewKalman():
    fr, rs = initFRRS()
    tgs = initAllUsefullObj(rs.sizeOfTarget[3], fr, rs)
    x, y = 0.1, 0.35
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    tgs.mac.setThetaMAC(theta)
    
    ii, saveD = 5, {}
    for i in range(5):
        tgs.tg.Ukf.setDelayUKF(ii)
        cost = tgs.tg.runTrajectory(x, y)
        for key, val in tgs.tg.SaveCoordVerif.items():
            WK = [el for el in val]
            UKF = [el for el in tgs.tg.SaveCoordUKF[key]]
        difTab = []
        for el1, el2 in zip(WK, UKF):
            a = np.sqrt((el1[0] - el2[0])**2 + (el1[1] - el2[1])**2)
            difTab.append(a)
        t = [i for i in range(len(difTab))]
        WKx, WKy, UKFx, UKFy = [x[0] for x in WK], [y[1] for y in WK], [x[0] for x in UKF], [y[1] for y in UKF]
        saveD[ii] = (WKx, WKy, UKFx, UKFy, difTab, t)
        ii += 5
    
    for key, val in saveD.items():
        print("key: ", key, " last yWK: ", val[1][len(val[1])-1], " last yUKF: ", val[3][len(val[3])-1])
    for key, val in saveD.items():
        plt.figure()
        plt.plot(val[0], val[1], c = 'b')
        plt.plot(val[2], val[3], c = 'r')
    plt.figure()
    for key, val in saveD.items():
        plt.plot(val[5], val[4])
    plt.show(block = True)
        
        
#testNewKalman()
    
    
    
    
    