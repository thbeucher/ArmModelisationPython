from FileProcessing.FileReading import *
from FileProcessing.FileSaving import *
from Regression.functionApproximator_LWR import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

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
print(fileR.uCommand["u1"])
print(len(fileR.uCommand["u1"]))
plt.figure()
plt.xlim(-1, 1)
plt.ylim(-1, 1)
a = plt.plot(range(10),range(10),color='red')
b = plt.plot(range(10),range(10),color='blue')
plt.xlabel('t [s]')
plt.ylabel('q1 [rad], q2[rad]')
red_patch = mpatches.Patch(color='red', label='q1')
blue_patch = mpatches.Patch(color='blue', label='q2')
plt.legend([a, b])
plt.title('Variations de q1 et q2 en fonction du temps')
plt.grid(True)
plt.show(block=True)

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot_wireframe([1,2,3,4,5], [0,2,4,8,9], [2,2.2,1.6,1.9,2])
plt.show(block=True)
    
    
    
    