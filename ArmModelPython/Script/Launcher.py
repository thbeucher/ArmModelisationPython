#######################################################################################
########## Author: Thomas Beucher // Module: Launcher #################################
#######################################################################################
from Script.Animation import animatAct
from Script.RunRegressionRBFN import runRBFN, test2DRBFN
from FileProcessing.FileReading import FileReading
from Optimisation.costFunction import costFunction
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
from FileProcessing.plotFunctions import costColorPlot

print("Scripts existants:\n -animation\n -rbfn\n -rbfn_test2D\n -genTraj\n -costColor\n")
choix = input("Veuillez entrer le choix du script à lancer: ")

if choix == "animation":
    ##Ce script permet de lancer l'animation de trajectoire de votre choix##
    animatAct()
    
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
    fra = FileReading()
    name = "RBFN2/" + str(nbfeat) + "feats/ThetaBIN"
    thetaa = fra.getobjread(name)
    cf = costFunction()
    res = cf.costFunctionRBFN2(thetaa)
    print(res)
    names = "RBFN2/" + str(nbfeat) + "feats/cout"
    namesb = "RBFN2/" + str(nbfeat) + "feats/coutBIN"
    fileSavingStr(names, res)
    fileSavingBin(names, res)
    
elif choix == "costColor":
    nbfeat = input("Nombre de features choisies: ")
    nbfeat = int(nbfeat)
    name = "RBFN2/" + str(nbfeat) + "feats/cout"
    costColorPlot(name)
    
    
    