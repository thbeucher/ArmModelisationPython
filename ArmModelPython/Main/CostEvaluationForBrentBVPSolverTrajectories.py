from Optimisation.costFunction import costFunction
from FileProcessing.FileReading import FileReading
from FileProcessing.FileSaving import fileSavingStr
import os


print("Debut de traitement!")
cf = costFunction()
#Chargement des donnees de trajectoire
fileR = FileReading()
stateAll, commandAll = fileR.recup_data(2)
a = 0
for i in range(int(len(fileR.data_store)/2)):
    if not str("trajectoire" + str(i+1+a) + "_command") in fileR.data_store:
        a += 1
    for j in range(len(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")])-1):
        cf.costFunctionJ(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")], 1, 0.002)
    cf.costFunctionJ(fileR.data_store[str("trajectoire" + str(i+1+a) + "_command")], 2, 0.002)
    name = "trajectoires_cout/trajectoire" + str(i+1+a) + "_cout"
    fileSavingStr(name, cf.Ju)
print("Fin de traitement!")
