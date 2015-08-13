#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: runScript

Description: main script to run what we want in the project
'''
import site
import os
from Main.Main import generateFromRBFN, generateFromCMAES, launchCMAESForAllTargetSizes #launchCMAESForSpecificTargetSize, generateResultsWithBestThetaTmp, launchCMAESWithBestThetaTmpForAllTargetSize,\ generateTrajectoryForScattergram

from Regression.RunRegressionRBFN import runRBFN
from Plot.TrajectoryAnimation import trajectoriesAnimation

from Plot.MuscularActivationsPlotFunctions import plotMuscularActivations
from Plot.plotFunctions import plotCostMapCMAES, plotCostMapRBFN, plotTimeDistanceTarget,\
    plotFittsLaw, plotPerfSizeDist, plotMapTimeTrajectories,plotScattergram,\
    plotVelocityProfiles, plotVelocityProfileBrent, plotXYPositionsBrent, plotArticularPositionsBrent

from Utils.UsefulFunctions import checkReachAllTarget

#------------------- install environment -----------------------------------------------------------------------------------

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

#----------------------------- main list of available actions ----------------------------------------------------------------------

def printMainMenu():
    print('Available scripts:')
    print('	Brent:')
    print('		1 plot velocity profiles')
    print('		2 plot articular positions')
    print('		3 plot XY positions')
    print('		4 plot muscular actuations (NOT AVAILABLE)')
    print('		5 (NOT AVAILABLE)')
    print('-------------------------------------------------')
    print('	RBFN:')
    print('		6 train from Brent data')
    print('		7 plot velocity profiles')
    print('		8 plot articular positions (NOT AVAILABLE)')
    print('		9 plot muscular actuations')
    print('		10 plot cost Map')
    print('-------------------------------------------------')
    print('	CMAES:')
    print('		11 train for all targets')
    print('		12 generate results from current controllers')
    print('		13 plot velocity profiles')
    print('		14 plot articular positions (NOT AVAILABLE)')
    print('		15 plot muscular actuations')
    print('		16 plot cost Map')                  
    print('		17 plot Time x Distance for Targets')                  
    print('		18 plot Size x Dist')                  
    print('		19 plot Fitts Law')                  
    print('		20 plot Map Time x Trajectory')
    print('		21 show trajectory animations')                 
    print('		22 plot Hit dispersion')

def runAll():
    runInstall()
    runChoice()

def runInstall():
    checkV = True
    choix = 0
    while checkV:
        try:
            c = input("Is it the first time you run the program? (0 = No, 1 = Yes) : ")
            c = int(c)
            if c == 0 or c == 1:
                checkV = False
        except:
            print("Enter 0 or 1")
    if c == 1:
        packageList = checkPackages()
        installMissingPackage(packageList)
    from distlib.compat import raw_input

def runChoice():
    checkL = True
    while checkL:
        try:
            printMainMenu()
            choix = input('Enter the number corresponding to the script you want to run: ')
            choix = int(choix)
            checkL = False
        except:
            print("Enter a number.")
    chooseFunction(choix)

def runAuto():
    for choix in range(21):
        chooseFunction(choix)

def chooseFunction(choix):
    if choix == 1:
        plotVelocityProfileBrent()
    elif choix == 2:
        plotArticularPositionsBrent()
    elif choix == 3:
        plotXYPositionsBrent()
    elif choix == 6:
        name = raw_input('Name of file to save the RBFN controller: ')
        runRBFN(name)

        nbret = input("Number of repeat for each trajectory (int): ")
        generateFromRBFN(nbret, name)
    elif choix == 7:
        nameF = raw_input('Folder where the results are saved: ')
        plotVelocityProfiles(nameF,True)
    elif choix == 9:
        nameF = raw_input('Folder where the results are saved: ')
        plotMuscularActivations(nameF,True)
    elif choix == 10:
        nameF = raw_input('Folder where the results are saved: ')
        plotCostMapRBFN(nameF)
        generateFromCMAES(nbret, nameTheta, name)
    elif choix == 11:
        launchCMAESForAllTargetSizes()
    elif choix == 12:
        nameTheta = raw_input('Name of the controller file: ')
        name = raw_input('Folder where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
    elif choix == 13:
        nameF = raw_input('Folder where the results are saved: ')
        plotVelocityProfiles(nameF,False)
    elif choix == 15:
        nameF = raw_input('Folder where the results are saved: ')
        plotMuscularActivations(nameF)
    elif choix == 16:
        nameF = raw_input('Folder where the results are saved: ')
        plotCostMapCMAES(nameF)
    elif choix == 17:
        nameF = raw_input('Folder where the results are saved: ')
        plotTimeDistanceTarget(nameF)
    elif choix == 18:
        nameF = raw_input('Folder where the results are saved: ')
        plotPerfSizeDist(nameF)
    elif choix == 19:
        nameF = raw_input('Folder where the results are saved: ')
        plotFittsLaw(nameF)
    elif choix == 20:
        nameF = raw_input('Folder where the results are saved: ')
        plotMapTimeTrajectories(nameF)
    elif choix == 21:
        rorc = input("enter 1 if cmaes results or 2 if rbfn results: ")
        rorc = int(rorc)
        nameF = raw_input('Folder where the results are saved: ')
        if rorc == 2:
            trajectoriesAnimation(nameF, True)
        elif rorc == 1:
            trajectoriesAnimation(nameF)
    elif choix == 22:
        nameF = raw_input('Folder where the results are saved: ')
        plotScattergram(nameF)
'''
JUNK

        else:
        st = input('Size of target: ')
        st = float(st)
        launchCMAESForSpecificTargetSize(st)
    elif choix == 14:
        nameF = raw_input('Folder where the results are saved: ')
        checkReachAllTarget(nameF)
    elif choix == 9:
        print("Generate results with the best theta temp !")
        nameF = raw_input('Folder where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
        generateResultsWithBestThetaTmp(nameF, nbret)
'''

    
runChoice()
#runAuto()
#generateFromRBFN(nbret, nameC)
