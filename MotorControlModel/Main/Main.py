'''
Author: Thomas Beucher

Module: NextStateComputation

Description: 
'''
import cma
import numpy as np
from multiprocessing.pool import Pool
from Utils.InitUtil import initFRRS
from Utils.ThetaNormalization import normalizationNP, matrixToVector


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




    
    
    
    
    
