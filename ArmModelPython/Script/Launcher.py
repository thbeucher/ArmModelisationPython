#######################################################################################
########## Author: Thomas Beucher // Module: Launcher #################################
#######################################################################################
from Script.Animation import animatAct
from Script.RunRegressionRBFN import runRBFN, test2DRBFN
from FileProcessing.FileReading import FileReading
from Optimisation.costFunction import costFunction
from FileProcessing.FileSaving import fileSavingStr

choix = input("Veuillez entrer le choix du script à lancer: ")

if choix == "animation":
    ##Ce script permet de lancer l'animation de trajectoire de votre choix##
    animatAct()
    
elif choix == "rbfn":
    #Ce script permet de lancer la regression sur l'ensemble des données de trajectoires Brent en mémoire
    nbfeat = input("Veuillez choisir le nombre de features: ")
    nbfeat = int(nbfeat)
    runRBFN(nbfeat)

elif choix =="rbfn_test2D":
    #Ce script lance le test de l'algorithme rbfn en dimension 2 pour visualiser les résultats
    nbfeat = input("Veuillez choisir le nombre de features: ")
    nbfeat = int(nbfeat)
    test2DRBFN(nbfeat)
    
elif choix == "genTraj":
    ##code permettant de lancer la fonction de génération de trajectoire
    fra = FileReading()
    thetaa = fra.getobjread("RBFN2/2feats/ThetaBIN")
    cf = costFunction()
    res = cf.costFunctionRBFN2(thetaa)
    print(res)
    fileSavingStr("RBFN2/2feats/cout", res)
    
    
    
    