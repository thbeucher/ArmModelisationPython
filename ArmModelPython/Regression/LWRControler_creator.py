from FileProcessing.FileReading import *
from FileProcessing.FileSaving import *
from Regression.functionApproximator_LWR import *


#Lecture des fichiers de trajectoire
fileR = FileReading()
fileR.recup_data()

#Boucle de traitement pour generer le controleur
i = 0
nbFeat = 10
funApprox = fa_lwr(nbFeat, fileR.data_store, fileR.name_store)
for el in fileR.name_store:
    fileR.tabActivationMuscu(el)
    #Boucle de traitement pour chaque activation musculaire
    k = 0
    while k < 6:
        funApprox.train_LWR(fileR.data_store[str(el + "_state")], fileR.uCommand[str("u" + str(k+1))])
        #Sauvegarder les donnees de regression dans un fichier
        nameToSave = el + "_u" + str(k+1) 
        fileSaving(nameToSave, funApprox.theta)
        k += 1
print("Fin du traitement!")

#Plot




    
    
    
    
    