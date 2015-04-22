'''
Author: Thomas Beucher

Module: Launcher 

Description: On retrouve dans ce fichier l'executable permetttant de lancer les differents scripts disponibles
'''

from Script.RunRegressionRBFN import runRBFN, test2DRBFN
from Utils.plotFunctions import costColorPlot, plotActivationMuscular,\
    plot_pos_ini, hitDispersion
from Optimisation.Cmaes import runCmaes
from Script.RunTrajectories import runGenTraj, runGenTrajCma
from Script.CostEvaluationForBrentBVPSolverTrajectories import costEvalBrent
from Utils.TrajectoriesAnimation import trajectoriesAnimation


print("Scripts existants:\n -animation        -posIni\n -rbfn             -costBrent\n -rbfn_test2D      -testResCma\n -genTraj          -hitDisp\n -costColor\n -actiMuscu\n -cmaes\n")
choix = input("Veuillez entrer le choix du script à lancer: ")

if choix == "animation":
    ##Ce script permet de lancer l'animation de trajectoire de votre choix##
    trajectoriesAnimation()
    
elif choix == "rbfn":
    #Ce script permet de lancer la regression sur l'ensemble des donnees de trajectoires Brent en memoire
    runRBFN()

elif choix =="rbfn_test2D":
    #Ce script lance le test de l'algorithme rbfn en dimension 2 pour visualiser les resultats
    nbfeat = input("Veuillez choisir le nombre de features: ")
    nbfeat = int(nbfeat)
    test2DRBFN(nbfeat)
    
elif choix == "genTraj":
    runGenTraj()
    
elif choix == "costColor":
    wha = input("Choisir les resultats a afficher(brent ou rbfn ou cma): ")
    costColorPlot(wha)
    
elif choix == "actiMuscu":
    wha = input("Choisir les activations musculaires a afficher (brent ou rbfn ou cma): ")
    plotActivationMuscular(wha)
    
elif choix == "cmaes":
    #Lance l'algorithme cmaes
    runCmaes()
    
elif choix == "posIni":
    plot_pos_ini()
    
elif choix == "costBrent":
    costEvalBrent()
    
    
elif choix == "testResCma":
    runGenTrajCma()
    
elif choix == "hitDisp":
    hitDispersion()
    
    
    
    
    
    