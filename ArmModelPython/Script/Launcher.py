from Script.Animation import animatAct
from Script.RunRegressionRBFN import runRBFN





choix = input("Veuillez entrer le choix du script à lancer: ")

if choix == "animation":
    ##Ce script permet de lancer l'animation de trajectoire de votre choix##
    animatAct()
    
elif choix == "rbfn":
    #Ce script permet de lancer la regression sur l'ensemble des données de trajectoires Brent en mémoire
    nbfeat = input("Veuillez choisir le nombre de features: ")
    nbfeat = int(nbfeat)
    runRBFN(nbfeat)