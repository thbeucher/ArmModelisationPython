#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

 
extensions = [
    Extension("GlobalVariables", ["MotorControlModelCython/GlobalVariables.pyx"]),
    Extension("runScript", ["MotorControlModelCython/runScript.pyx"]),
    Extension("ArmDynamics", ["MotorControlModelCython/ArmModel/ArmDynamics.pyx"]),
    Extension("ArmParameters", ["MotorControlModelCython/ArmModel/ArmParameters.pyx"]),
    Extension("GeometricModel", ["MotorControlModelCython/ArmModel/GeometricModel.pyx"]),
    Extension("MusclesParameters", ["MotorControlModelCython/ArmModel/MusclesParameters.pyx"]),
    Extension("MuscularActivationCommand", ["MotorControlModelCython/ArmModel/MuscularActivationCommand.pyx"]),
    Extension("CostComputation", ["MotorControlModelCython/CostComputation/CostComputation.pyx"]),
    Extension("NextStateComputation", ["MotorControlModelCython/CostComputation/NextStateComputation.pyx"]),
    Extension("Main", ["MotorControlModelCython/Main/Main.pyx"]),
    Extension("functionApproximator_RBFN", ["MotorControlModelCython/Regression/functionApproximator_RBFN.pyx"]),
    Extension("runExperimentalSetupTrajectories", ["MotorControlModelCython/runExperimentalSetupTrajectories/runExperimentalSetupTrajectories.pyx"]),
    Extension("ChangeExperimentalSetup", ["MotorControlModelCython/Script/ChangeExperimentalSetup.pyx"]),
    Extension("RunRegressionRBFN", ["MotorControlModelCython/Script/RunRegressionRBFN.pyx"]),
    Extension("TrajectoryGenerator", ["MotorControlModelCython/TrajectoryGenerator/TrajectoryGenerator.pyx"]),
    Extension("UnscentedKalmanFilterControl", ["MotorControlModelCython/UnscentedKalmanFilterControl/UnscentedKalmanFilterControl.pyx"]),
    Extension("CartesianProduct", ["MotorControlModelCython/Utils/CartesianProduct.pyx"]),
    Extension("CreateVectorUtil", ["MotorControlModelCython/Utils/CreateVectorUtil.pyx"]),
    Extension("DataNormalization", ["MotorControlModelCython/Utils/DataNormalization.pyx"]),
    Extension("FileReading", ["MotorControlModelCython/Utils/FileReading.pyx"]),
    Extension("FileSaving", ["MotorControlModelCython/Utils/FileSaving.pyx"]),
    Extension("FunctionsUsefull", ["MotorControlModelCython/Utils/FunctionsUsefull.pyx"]),
    Extension("InitUtil", ["MotorControlModelCython/Utils/InitUtil.pyx"]),
    Extension("InitUtilMain", ["MotorControlModelCython/Utils/InitUtilMain.pyx"]),
    Extension("NiemRoot", ["MotorControlModelCython/Utils/NiemRoot.pyx"]),
    Extension("plotFunctions", ["MotorControlModelCython/Utils/plotFunctions.pyx"]),
    Extension("PurgeData", ["MotorControlModelCython/Utils/PurgeData.pyx"]),
    Extension("ReadDataTmp", ["MotorControlModelCython/Utils/ReadDataTmp.pyx"]),
    Extension("ReadSetupFile", ["MotorControlModelCython/Utils/ReadSetupFile.pyx"]),
    Extension("StateVectorUtil", ["MotorControlModelCython/Utils/StateVectorUtil.pyx"]),
    Extension("ThetaNormalization", ["MotorControlModelCython/Utils/ThetaNormalization.pyx"])
]
 
setup(
    cmdclass = {'build_ext':build_ext},
    ext_modules = cythonize(extensions),
)



