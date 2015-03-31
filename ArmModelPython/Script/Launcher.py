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

print("Scripts existants:\n -animation        -posIni\n -rbfn             -costBrent\n -rbfn_test2D\n -genTraj\n -costColor\n -actiMuscu\n -cmaes\n")
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
    ##code permettant de lancer la fonction de generation de trajectoire
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    noise = input("Avec bruit moteur? (Y or N): ")
    print("(0: Rien / 1: U / 2: Unoise / 3: CoordTrajU / 4: CoordTrajUnoise / 5: nbIte")
    sauv = input("Que voulez vous sauvegarder?: ")
    sauv = int(sauv)
    fra = FileReading()
    nbtra = input("Sur combien de trajectoire voulez vous le theta(12 ou X): ")
    if nbtra == "12":
        name = "RBFN2/" + str(nbfeat) + "feats/ThetaBIN"
        names = "RBFN2/" + str(nbfeat) + "feats/cout"
        namesb = "RBFN2/" + str(nbfeat) + "feats/coutBIN"
        if noise == "Y":
            cf = costFunction(nbfeat, 1, 1, sauv)
        elif noise == "N":
            cf = costFunction(nbfeat, 1, 0, sauv)
    elif nbtra == "X":
        name = "RBFN2/" + str(nbfeat) + "feats/ThetaXBIN"
        names = "RBFN2/" + str(nbfeat) + "feats/coutX"
        names2 = "RBFN2/" + str(nbfeat) + "feats/coutXBIN"
        namesb = "RBFN2/" + str(nbfeat) + "feats/coutXBIN"
        if noise == "Y":
            cf = costFunction(nbfeat, 0, 1, sauv)
        elif noise == "N":
            cf = costFunction(nbfeat, 0, 0, sauv)
    thetaa = fra.getobjread(name)
    res = cf.costFunctionRBFN2(thetaa)
    print(res)
    fileSavingStr(names, res)
    fileSavingBin(names2, res)
    
elif choix == "costColor":
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    name = "RBFN2/" + str(nbfeat) + "feats/coutX"
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
    
    
    
    
    
    
    
    
    