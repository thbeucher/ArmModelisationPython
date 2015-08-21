#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher + Olivier Sigaud

Module: runScript

Description: main script to run what we want in the project
'''

from Main.Main import generateFromRBFN, generateFromCMAES, generateCostMapFromRBFN, generateCostMapFromCMAES, launchCMAESForAllTargetSizes, launchCMAESForSpecificTargetSize

from Regression.RunRegressionRBFN import runRBFN, UnitTest, UnitTestRBFNController, UnitTestArmModel


from Plot.plotFunctions import trajectoriesAnimation, plotCostColorMap, plotTimeColorMap, plotTimeDistanceTarget, plotFittsLaw, plotPerfSizeDist, plotVelocityProfile, plotXYPositions, plotArticularPositions, plotInitPos, plotMuscularActivations, plotScattergram, plotHitDispersion, plotExperimentSetup, plotCMAESCostProgress

from Utils.Chrono import Chrono

#----------------------------- main list of available actions ----------------------------------------------------------------------

def printMainMenu():
    print('Available scripts:')
    print('	Brent:')
    print('		1 plot velocity profiles')
    print('		2 plot articular positions')
    print('		3 plot XY positions')
    print('		4 plot muscular activations')
    print('-------------------------------------------------')
    print('	RBFN:')
    print('		5 train from Brent data')
    print('		6 generate results from RBFN controller')
    print('		7 plot velocity profiles')
    print('		8 plot XY positions')
    print('		9 plot muscular activations')
    print('		10 plot cost Map')
    print('-------------------------------------------------')
    print('	CMAES:')
    print('		11 train CMAES for all targets')
    print('		12 generate results from CMAES controllers')
    print('		13 plot velocity profiles')
    print('		14 plot articular positions')
    print('		15 plot muscular activations')
    print('		16 plot cost Map')                  
    print('		17 plot Time x Distance for Targets')                  
    print('		18 plot Size x Dist')                  
    print('		19 plot Fitts Law')                  
    print('		20 plot Map Time x Trajectory')
    print('		21 show trajectory animations (all)')                 
    print('		22 plot Hit dispersion (CMAES or RBFN)')
    print('		23 train CMAES for one target')
    print('		24 plot CMAES cost progress')
    print('		25 generate rich results from RBFN controller')
    print('		26 generate rich results from CMAES controllers')

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
        plotVelocityProfile("Brent")
    elif choix == 2:
        plotArticularPositions("Brent")
    elif choix == 3:
        plotXYPositions("Brent")
    elif choix == 4:
        plotMuscularActivations("Brent")
    elif choix == 5:
        name = raw_input('Name of file to save the RBFN controller: ')
        c = Chrono()
        runRBFN(name)
        c.stop()

    elif choix == 6:
        name = raw_input('Name of the RBFN controller file: ')
        fname = raw_input('Folder where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        c = Chrono()
        generateFromRBFN(nbret, name, fname)
        c.stop()
    elif choix == 7:
        nameF = raw_input('Folder where the results are saved: ')
        plotVelocityProfile("RBFN",nameF)
    elif choix == 8:
        nameF = raw_input('Folder where the results are saved: ')
        rorc = input("enter 1 if XY or 2 if Joint results: ")
        rorc = int(rorc)
        if rorc == 1:
            plotXYPositions("RBFN",nameF)
        else:
            plotArticularPositions("RBFN",nameF)
    elif choix == 9:
        nameF = raw_input('Folder where the results are saved: ')
        plotMuscularActivations("RBFN",nameF)
    elif choix == 10:
        nameF = raw_input('Folder where the results are saved: ')
        plotCostColorMap("RBFN",nameF)
    elif choix == 11:
        rorc = input("enter 1 if from RBFN, anything if from previous CMAES: ")
        save = False
        rorc = int(rorc)
        if rorc == 1:
            save = True
        name = raw_input('Name of the controller file: ')
        c = Chrono()
        launchCMAESForAllTargetSizes(name,save)
        c.stop()
    elif choix == 12:
        nameTheta = raw_input('Name of the controller file: ')
        name = raw_input('Folder where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
        c = Chrono()
        generateFromCMAES(nbret, nameTheta, name)
        c.stop()
    elif choix == 13:
        nameF = raw_input('Folder where the results are saved: ')
        plotVelocityProfile("CMAES",nameF)
    elif choix == 14:
        nameF = raw_input('Folder where the results are saved: ')
        tSize = raw_input('Target Size: ')
        rorc = input("enter 1 if XY or 2 if Joint results: ")
        rorc = int(rorc)
        if rorc == 1:
            plotXYPositions("CMAES",nameF,tSize)
        else:
            plotArticularPositions("CMAES",nameF,tSize)
    elif choix == 15:
        nameF = raw_input('Folder where the results are saved: ')
        tSize = raw_input('Target Size: ')
        plotMuscularActivations("CMAES",nameF,tSize)
    elif choix == 16:
        nameF = raw_input('Folder where the results are saved: ')
        #tSize = raw_input('Target Size: ')
        #plotCostColorMap("CMAES",nameF,tSize)
        plotCostColorMap("CMAES",nameF)
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
        plotTimeColorMap("CMAES",nameF)
    elif choix == 21:
        rorc = input("enter 0 if Brent, 1 if RBFN or 2 if CMAES results: ")
        rorc = int(rorc)
        if rorc == 0:
            trajectoriesAnimation("Brent")
        elif rorc == 1:
            nameF = raw_input('Folder where the results are saved: ')
            trajectoriesAnimation("RBFN",nameF)
        elif rorc == 2:
            nameF = raw_input('Folder where the results are saved: ')
            tSize = raw_input('Target Size: ')
            trajectoriesAnimation("CMAES",nameF, tSize)
    elif choix == 22:
        nameF = raw_input('Folder where the results are saved: ')
        rorc = input("enter 1 if RBFN or 2 if CMAES results: ")
        #plotHitDispersion(nameF,"0.05")
        rorc = int(rorc)
        if rorc == 1:
            plotScattergram("RBFN",nameF)
        elif rorc == 2:
            plotScattergram("CMAES",nameF)

    elif choix == 23:
        name = raw_input('Name of the controller file: ')
        rorc = input("enter 1 if from RBFN, anything if from previous CMAES: ")
        save = False
        rorc = int(rorc)
        if rorc == 1:
            save = True
        tSize = raw_input('Target Size: ')
        c = Chrono()
        launchCMAESForSpecificTargetSize(float(tSize),name,save)
        c.stop()
    elif choix == 24:
        plotCMAESCostProgress()
    elif choix == 25:
        name = raw_input('Name of the RBFN controller file: ')
        fname = raw_input('Folder where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        c = Chrono()
        generateCostMapFromRBFN(nbret, name, fname)
        c.stop()
    elif choix == 26:
        nameTheta = raw_input('Name of the controller file: ')
        name = raw_input('Folder where you want to save the results: ')
        nbret = input("Number of repeat for each trajectory (int): ")
        nbret = int(nbret)
        c = Chrono()
        generateCostMapFromCMAES(nbret, nameTheta, name)
        c.stop()

#plotInitPos()  
#runAuto()
#generateFromRBFN(nbret, nameC)
runChoice()

#UnitTest()
#UnitTestRBFNController()
#UnitTestArmModel()
#plotExperimentSetup()
