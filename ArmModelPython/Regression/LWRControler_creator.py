from FileProcessing.FileReading import *
from FileProcessing.FileSaving import *
from Regression.functionApproximator_LWR import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

'''#Lecture des fichiers de trajectoire
fileR = FileReading()
fileR.recup_data()

#Boucle de traitement pour generer le controleur
i = 0
nbFeat = 7
funApprox = fa_lwr(nbFeat, fileR.data_store, fileR.name_store)
for el in fileR.name_store:
    fileR.tabActivationMuscu(el)
    #Boucle de traitement pour chaque activation musculaire
    k = 0
    print(el)
    while k < 6:
        funApprox.train_LWR(fileR.data_store[str(el + "_state")], fileR.uCommand[str("u" + str(k+1))])
        #Sauvegarder les donnees de regression dans un fichier
        nameToSave = el + "_u" + str(k+1) 
        fileSaving(nameToSave, funApprox.theta)
        k += 1
print("Fin du traitement!")'''

#x_values = fileR.data_store["trajectoire1_state"]
#y_approx = funApprox.functionApproximatorOutput(x_values)
#f_approx = plt.plot(x_values, y_approx, 'r')

#Plot

'''q1 = []
q2 = []
qq1 = []
qq2 = []
for el in fileR.data_store["trajectoire1_state"]:
    qq1.append(el[0])
    qq2.append(el[1])
    q1.append(el[2])
    q2.append(el[3])

plt.figure()
a = plt.plot(qq1,fileR.uCommand["u1"],color='red')
b = plt.plot(qq1,y_approx,color='blue')
plt.title('qq1')
plt.figure()
a = plt.plot(qq2,fileR.uCommand["u1"],color='red')
plt.title('qq2')
plt.figure()
a = plt.plot(q2,fileR.uCommand["u1"],color='red')
plt.title('q2')

plt.figure()
#plt.xlim(-1, 1)
#plt.ylim(-1, 1)
a = plt.plot(q1,fileR.uCommand["u1"],color='red')
#b = plt.plot(range(10),range(10),color='blue')
#plt.xlabel('t [s]')
#plt.ylabel('q1 [rad], q2[rad]')
#red_patch = mpatches.Patch(color='red', label='q1')
#blue_patch = mpatches.Patch(color='blue', label='q2')
#plt.legend([a, b])
plt.title('q1')
plt.grid(True)
plt.show(block=True)'''

#####################################################################################
#Test en dimension 2
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = X**2 + Y**2
xData = []
zData = []
for i in range(len(X)):
    for j in range(len(X)):
        xData.append((X[i][j],Y[i][j]))
        zData.append(Z[i][j])
nbFeat2 = 5
funApproxDim2 = fa_lwr(nbFeat2, xData, zData)
funApproxDim2.train_LWR(xData, zData)
print(funApproxDim2.theta.shape)
print(funApproxDim2.theta)

y_approx = funApproxDim2.functionApproximatorOutput(xData)
print("yapprox: ", y_approx.shape)
y_approxMat = np.zeros((40,40))
for i in range(len(X)):
    for j in range(len(X)):
        y_approxMat[i][j] = y_approx[40*(i-1)+j]
print("ymat: ", y_approxMat.shape)
#f_approx = plt.plot(x_values, y_approx, 'r')
#####################################################################################

fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = X**2 + Y**2
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0, antialiased=False)

fig2 = plt.figure()
ax = fig2.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
surf = ax.plot_surface(X, Y, y_approxMat, rstride=1, cstride=1, linewidth=0, antialiased=False)
plt.show(block=True)
    
    
    
    