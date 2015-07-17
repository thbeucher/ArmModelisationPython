#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: initUtilMain

Description: Here some functions which initializes objects usefull to generate trajectory
'''
import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

from ArmParameters import ArmParameters
from MusclesParameters import MusclesParameters
from ArmDynamics import ArmDynamics
from functionApproximator_RBFN import fa_rbfn
from MuscularActivationCommand import MuscularActivationCommand
from UnscentedKalmanFilterControl import UnscentedKalmanFilterControl
from TrajectoryGenerator import TrajectoryGenerator
from runExperimentalSetupTrajectories import TrajectoriesGenerator
from CostComputation import CostComputation
from NextStateComputation import NextStateComputation
from GlobalVariables import pathTrajectoriesFolder


cpdef object initController(object rs, object fr):
    '''
	Initializes the controller allowing to compute the output from the input and the vector of parameters theta
	
	Input:		-rs: ReadSetup, class object
				-fr, FileReading, class object
	'''
    cdef:
        object fa
        dict state
        dict command
        np.ndarray[DTYPE_t, ndim=2] stateAll
        np.ndarray[DTYPE_t, ndim=2] commandAll
    #Initializes the function approximator with the number of feature used
    fa = fa_rbfn(rs.numfeats)
    #Get state and command to initializes the controller by putting the features
    state, command = fr.getData(pathTrajectoriesFolder)
    #Transform data from dictionnary to numpy array
    stateAll, commandAll = fr.dicToArray(state), fr.dicToArray(command)
    #Set the data
    fa.setTrainingData(stateAll.T, commandAll.T)
    #set the center and width for the features
    fa.setCentersAndWidths()
    return fa

cpdef object initAllUsefullObj(double sizeOfTarget, object fr, object rs, bint save = False):
    '''
	Initializes class object needed to generate trajectories
	
	Input:		-sizeOfTarget: the size of the target, float
				-fr, FileReading, class object
				-rs, ReadSetup, class object
	'''
    cdef:
        object fa
        object mac
        object armP
        object musclesP
        object armD
        object nsc
        object Ukf
        object cc
        object tg
        object tgs
    #fa, function approximator ie the controller
    fa = initController(rs, fr)
    #mac,muscular activation command ie the class which compute the next muscular activation vector
    mac = MuscularActivationCommand()
    mac.initParametersMAC(fa, rs)
    #arm parameters
    armP = ArmParameters()
    #muscules parameters
    musclesP = MusclesParameters()
    #arm dynamics
    armD = ArmDynamics()
    armD.initParametersAD(armP, musclesP, rs.dt)
    #nsc, next state computation
    nsc = NextStateComputation()
    nsc.initParametersNSC(mac, armP, rs, musclesP)
    #ukf, unscented kalman filter
    Ukf = UnscentedKalmanFilterControl()
    #6 is the dimension of the state for the filter, 4 is the dimension of the observation for the filter, 25 is the delay used
    Ukf.initParametersUKF(rs.dimStateUKF, rs.dimObsUKF, rs.delayUKF, nsc, armD, mac)
    #cc, cost computation
    cc = CostComputation()
    cc.initParametersCC(rs)
    #tg, trajectory generator
    tg = TrajectoryGenerator()
    tg.initParametersTG(armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac, save)
    #tgs, trajectories generator
    tgs = TrajectoriesGenerator()
    #here 5 is the number of repeat of each trajectory, 4 is the dimension of the input, 6 is the dimension of the ouput
    tgs.initParametersTGS(rs, rs.numberOfRepeatEachTraj, tg, rs.inputDim, rs.outputDim, mac)
    return tgs
