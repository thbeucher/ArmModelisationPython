from FileProcessing.FileReading import *
from FileProcessing.FileSaving import *
from Regression.functionApproximator_LWR import *


#Lecture des fichiers de trajectoire
fileR = FileReading()
nameFile, nbFile = fileR.recup_data()

#Boucle de traitement pour generer le controleur
i = 0
nbFeat = 10
funApprox = fa_lwr(nbFeat)
while i < nbFile:
    nameFileTemp = nameFile + str(i+1)
    fileR.tabActivationMuscu(i, nameFileTemp)
    #Boucle de traitement pour chaque activation musculaire
    k = 0
    while k < 6:
        funApprox.train_LWR(fileR.data_store[str(nameFileTemp + "_state")], fileR.uCommand[str("u" + str(k+1))])
        #Sauvegarder les donnees de regression dans un fichier
        nameToSave = nameFileTemp + "_u" + str(k+1) 
        fileSaving(nameToSave, funApprox.theta)
        k += 1
    i += 1
    
    
    
    
    
    