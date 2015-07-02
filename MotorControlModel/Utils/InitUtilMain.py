'''
Author: Thomas Beucher

Module: initUtilMain

Description: 
'''
from ArmModel.ArmParameters import ArmParameters
from ArmModel.MusclesParameters import MusclesParameters
from ArmModel.ArmDynamics import ArmDynamics
from Regression.functionApproximator_RBFN import fa_rbfn


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
    Ukf.initParametersUKF(6, 4, 25, nsc, armD, mac)
    cc = CostComputation()
    cc.initParametersCC(rs)
    tg = TrajectoryGenerator()
    tg.initParametersTG(armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac)
    tgs = TrajectoriesGenerator()
    tgs.initParametersTGS(rs, 5, tg, 4, 6, mac)
    return tgs
