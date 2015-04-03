'''
Author: Thomas Beucher
Module: Launcher 
'''
from Script.Animation import animatAct
from Script.RunRegressionRBFN import runRBFN, test2DRBFN
from FileProcessing.FileReading import FileReading
from Optimisation.costFunction import costFunction
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
from FileProcessing.plotFunctions import costColorPlot, plotActivationMuscular,\
    plot_pos_ini
from Optimisation.Cmaes import runCmaes
from matplotlib.mlab import griddata
from Main.CostEvaluationForBrentBVPSolverTrajectories import costEvalBrent
from Script.RunTrajectories import runGenTraj

print("Scripts existants:\n -animation        -posIni\n -rbfn             -costBrent\n -rbfn_test2D      -testResCma\n -genTraj\n -costColor\n -actiMuscu\n -cmaes\n")
choix = input("Veuillez entrer le choix du script à lancer: ")

if choix == "animation":
    ##Ce script permet de lancer l'animation de trajectoire de votre choix##
    nbfeat = input("Veuillez choisir le nombre de features: ")
    nbfeat = int(nbfeat)
    animatAct(nbfeat)
    
elif choix == "rbfn":
    #Ce script permet de lancer la regression sur l'ensemble des donnees de trajectoires Brent en memoire
    nbfeat = input("Veuillez choisir le nombre de features: ")
    nbfeat = int(nbfeat)
    runRBFN(nbfeat)

elif choix =="rbfn_test2D":
    #Ce script lance le test de l'algorithme rbfn en dimension 2 pour visualiser les resultats
    nbfeat = input("Veuillez choisir le nombre de features: ")
    nbfeat = int(nbfeat)
    test2DRBFN(nbfeat)
    
elif choix == "genTraj":
    runGenTraj()
    
elif choix == "costColor":
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    name = "RBFN2/" + str(nbfeat) + "feats/coutXBIN"
    wha = input("Choisir les resultats a afficher(brent ou rbfn): ")
    costColorPlot(name, wha)
    
elif choix == "actiMuscu":
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    wha = input("Choisir les activations musculaires a afficher (brent ou RBFN): ")
    plotActivationMuscular(wha, nbfeat)
    
elif choix == "cmaes":
    #Lance l'algorithme cmaes
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    runCmaes(nbfeat)
    
elif choix == "posIni":
    plot_pos_ini()
    
elif choix == "costBrent":
    costEvalBrent()
    
    
elif choix == "testResCma":
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    fr = FileReading()
    theta = fr.getobjread("OptimisationResults/thetaSolBIN")
    maxT = fr.getobjread("OptimisationResults/maxTBIN")
    cf = costFunction(nbfeat)
    cf.recupMaxThetaN(maxT)
    cf.costFunctionCMAES(theta)
    
    
    
    
    
    
    
    