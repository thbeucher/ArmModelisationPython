#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: runScript

Description: main script to run what we want in the project
'''
import site
import os
from Main.Main import launchCMAESForSpecificTargetSize, launchCMAESForAllTargetSize, generateResults,\
    generateResultsWithBestThetaTmp, launchCMAESWithBestThetaTmpForAllTargetSize,\
    generateTrajectoryForScattergram, generateResultsRBFN

from Script.RunRegressionRBFN import runRBFN
from Script.TrajectoryAnimation import trajectoriesAnimation

from Plot.MuscularActivationsPlotFunctions import plotMuscularActivations
from Plot.plotFunctions import plotAllCmaes, plotTimeDistanceTarget,\
    plotFittsLaw, plotPerfSizeDist, plotMapTimeTrajectories,\
    plotVelocityProfilesCMAES

from Utils.UsefulFunctions import checkReachAllTarget


def checkPackages():
    a = site.getsitepackages()
    packageList = os.listdir(a[0])
    packageNeeded = {}
    listOfPackageNeeded = ['pykalman', 'cma', 'cython']
    for el in listOfPackageNeeded:
        packageNeeded[el] = 0
    for el1 in listOfPackageNeeded:
        for el2 in packageList:
            if el1 in el2:
                packageNeeded[el1] = 1
    print(packageNeeded)    
    return packageNeeded

def installMissingPackage(packageList):
    a = site.getsitepackages()
    a = a[0]
    a = a.split('/')
    for el in a:
        if 'python' in el:
            b = el.replace('python', '')
            b = int(float(b))
    os.system('sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose')
    if b == 2:
        try:
            os.system('sudo easy_install numpy scipy Sphinx numpydoc nose pykalman')
            os.system('sudo pip install cma')
            os.system('sudo easy_install cython')
            os.system('sudo pip install distlib')
        except:
            pass
    elif b == 3:
        try:
            os
            os.system('sudo easy_install3 numpy scipy Sphinx numpydoc nose pykalman')
            os.system('sudo pip3 install cma')
            os.system('sudo easy_install3 cython')
            os.system('sudo pip3 install distlib')
        except:
            pass
    os.system('clear')

def runAll():
    checkV = True
    checkL = True
    choix = 0
    while checkV:
        try:
            c = input("is it the first time you run the program? (0 = No, 1 = Yes) : ")
            c = int(c)
            if c == 0 or c == 1:
                checkV = False
        except:
            print("Enter 0 or 1")
    if c == 1:
        packageList = checkPackages()
        installMissingPackage(packageList)
    from distlib.compat import raw_input
    while checkL:
        try:
            print('Script available: 1_launchCMAESForSpecificTargetSize\n                  2_launchCMAESForAllTargetSize\n                  3_generateResults\n                  4_plotAllCmaes\n                  5_plotTimeDistanceTarget\n                  6_plotFittsLaw\n                  7_plotPerfSizeDist\n                  8_plotMapTimeTrajectories\n                  9_generateResultsWithBestThetaTmp\n                  10_launchCMAESWithBestThetaTmpForAllTargetSize\n                  11_plotForAllTargetVelocityProfile\n                  12_runRBFN\n                  13_generateTrajectoryForScattergram')
            print('                  15_generateResultsRBFN\n                  16_plotRbfnResults\n                  17_trajectoriesAnimation\n')
            choix = input('Enter the number corresponding to the script you want to run: ')
            choix = int(choix)
            checkL = False
        except:
            print("Enter a number.")
    if choix == 1:
        st = input('Size of target: ')
        st = float(st)
        launchCMAESForSpecificTargetSize(st)
    elif choix == 2:
        launchCMAESForAllTargetSize()
    elif choix == 3:
        nameF = raw_input('Folder name where you want to save the results: ')
        nameT = raw_input('Number at the end of the name of the theta file: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
        generateResults(nameF, nbret, nameT)
    elif choix == 4:
        nameF = raw_input('Folder name where the results are saved: ')
        plotAllCmaes(nameF)
    elif choix == 5:
        nameF = raw_input('Folder name where the results are saved: ')
        plotTimeDistanceTarget(nameF)
    elif choix == 6:
        nameF = raw_input('Folder name where the results are saved: ')
        plotFittsLaw(nameF)
    elif choix == 7:
        nameF = raw_input('Folder name where the results are saved: ')
        plotPerfSizeDist(nameF)
    elif choix == 8:
        nameF = raw_input('Folder name where the results are saved: ')
        plotMapTimeTrajectories(nameF)
    elif choix == 9:
        print("Generate results with the best theta temp !")
        nameF = raw_input('Folder name where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
        generateResultsWithBestThetaTmp(nameF, nbret)
    elif choix == 10:
        launchCMAESWithBestThetaTmpForAllTargetSize()
    elif choix == 11:
        nameF = raw_input('Folder name where the results are saved: ')
        plotForAllTargetVelocityProfile(nameF)
    elif choix == 12:
        nameC = raw_input('Name to save the RBFN controller: ')
        runRBFN(nameC)
    elif choix == 13:
        nameF = raw_input('Folder name where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
        nameT = raw_input('Number at the end of the name of the theta file: ')
        generateTrajectoryForScattergram(nameF, nbret, nameT)
    elif choix == 14:
        nameF = raw_input('Folder name where the results are saved: ')
        checkReachAllTarget(nameF)
    elif choix == 15:
        nameF = raw_input('Folder name where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
        nameT = raw_input('Name of the theta file to use: ')
        generateResultsRBFN(nameF, nbret, nameT)
    elif choix == 16:
        nameF = raw_input('Folder name where the results are saved: ')
        plotForAllTargetVelocityProfile(nameF, True)
        plotAllCmaes(nameF, True)
        #plotTimeDistanceTarget(nameF, True)
        #plotFittsLaw(nameF, True)
        #plotPerfSizeDist(nameF, True)
        plotMapTimeTrajectories(nameF, True)
    elif choix == 17:
        rorc = input("enter 1 if cmaes results or 2 if rbfn results: ")
        rorc = int(rorc)
        nameF = raw_input('Folder name where the results are saved: ')
        if rorc == 2:
            trajectoriesAnimation(nameF, True)
        elif rorc == 1:
            trajectoriesAnimation(nameF)
    elif choix == 18:
        rorc = input("enter 1 if cmaes results or 2 if rbfn results: ")
        rorc = int(rorc)
        nameF = raw_input('Folder name where the results are saved: ')
        if rorc == 2:
            plotMuscularActivations(nameF, True)
        elif rorc == 1:
            plotActiMuscu(nameF)
    
runAll()



