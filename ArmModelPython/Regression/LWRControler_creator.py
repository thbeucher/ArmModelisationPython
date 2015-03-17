from FileProcessing.FileReading import *
from FileProcessing.FileSaving import *
from Regression.functionApproximator_LWR import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import axes3d
import time

#Lecture des fichiers de trajectoire
fileR = FileReading()
stateAll, commandAll = fileR.recup_data()
print("state", stateAll.shape, "command", commandAll.shape)

#Boucle de traitement pour generer le controleur
i = 0
nbFeat = 3
print("Debut de traitement trajectoire par trajectoire!")
t0 = time.time()
funApprox = fa_lwr(nbFeat, 4, fileR.data_store, fileR.name_store, 3)
fileSaving("xMinMax", funApprox.xMinxMax, funApprox.nbFeat)
for el in fileR.name_store:
    fileR.tabActivationMuscu(el)
    #Boucle de traitement pour chaque activation musculaire
    k = 0
    print(el)
    while k < 6:
        funApprox.train_LS(fileR.data_store[str(el + "_state")], fileR.uCommand[str(el + "_u" + str(k+1))])
        #Sauvegarder les donnees de regression dans un fichier
        nameToSave = el + "_u" + str(k+1) 
        fileSaving(nameToSave, funApprox.thetaLS, funApprox.nbFeat)
        k += 1
t1 = time.time()
print("Fin du traitement trajectoire par trajectoire! (Temps de traitement: ", (t1 - t0), "s)")
print("Debut traitement toutes les trajectoires ensembles!")
t0 = time.time()
fileR.tabActivationMuscu("AllCommand", commandAll, True)
for i in range(6):
    name = str("AllCommand_u" + str(i+1))
    funApprox.train_LS(stateAll, fileR.uCommand[name])
    fileSaving(name, funApprox.thetaLS, funApprox.nbFeat)
t1 = time.time()
print("Fin de traitement toutes les trajectoires ensembles! (Temps de traitement: ", (t1 - t0), "s)")

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
'''X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
xData = []
zData = []
for i in range(len(X)):
    for j in range(len(X)):
        xData.append((X[i][j],Y[i][j]))
        zData.append(Z[i][j])
nbFeat2 = 15
funApproxDim2 = fa_lwr(nbFeat2, False, False, 2)
funApproxDim2.train_LWR(xData, zData)
print("Theta shape: ",funApproxDim2.theta.shape)
#print(funApproxDim2.theta)

y_approx = funApproxDim2.functionApproximatorOutput(xData)
print("yapprox shape: ", y_approx.shape)
y_approxMat = np.zeros((len(X),len(X)))
for i in range(len(X)):
    for j in range(len(X)):
        y_approxMat[i][j] = y_approx[len(X)*i+j]
print("ymat: ", y_approxMat.shape)
print("width: ", funApproxDim2.widthConstant)
#####################################################################################
fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0, antialiased=False)

fig2 = plt.figure()
ax = fig2.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
surf = ax.plot_surface(X, Y, y_approxMat, rstride=1, cstride=1, linewidth=0, antialiased=False)


fig3 = plt.figure()
ax = fig3.add_subplot(111, projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Ztmp = []
Xtmp = np.zeros((10,10))
Ytmp = np.zeros((10,10))
for i in range(3):
    for j in range(3):
        Ztmp.append((funApproxDim2.centersXt[i][j], funApproxDim2.centersYt[i][j]))
for el in Ztmp:
    #for i in range(10):
        #for j in range(10):
            #Xtmp[i][j] = X[i][j]
            #Ytmp[i][j] = Y[i][j]

    Z = np.exp(-(np.divide(np.square(X - el[0]), funApproxDim2.widthConstant) 
                    + np.divide(np.square(Y - el[1]), funApproxDim2.widthConstant)))
    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0, antialiased=False)
#Z = np.sin(np.sqrt(X**2 + Y**2))
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
ax.scatter(funApproxDim2.centersXt,funApproxDim2.centersYt,0, color = 'r')


fig4 = plt.figure()
ax = fig4.add_subplot(111, projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
ax.plot_wireframe(X, Y, y_approxMat, rstride=10, cstride=10)
for i in range(nbFeat2):
    for j in range(nbFeat2):
        ax.plot([funApproxDim2.centersXt[i][j]-funApproxDim2.widthConstant/2, funApproxDim2.centersXt[i][j]+funApproxDim2.widthConstant/2], [funApproxDim2.centersYt[i][j],funApproxDim2.centersYt[i][j]], 0)
        ax.plot([funApproxDim2.centersXt[i][j],funApproxDim2.centersXt[i][j]], [funApproxDim2.centersYt[i][j]-funApproxDim2.widthConstant/2, funApproxDim2.centersYt[i][j]+funApproxDim2.widthConstant/2], 0)


plt.show(block=True)'''









###################################################################################################################################
##TEST LS
###################################################################################################################################
'''X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
xData = []
zData = []
for i in range(len(X)):
    for j in range(len(X)):
        xData.append((X[i][j],Y[i][j]))
        zData.append(Z[i][j])
nbFeat2 = 20
funApproxDim2 = fa_lwr(nbFeat2, False, False, 2)
funApproxDim2.train_LS(xData, zData)
y_approxLS = funApproxDim2.functionApproximatorOutputLS(xData)
y_approxMatLS = np.zeros((len(X),len(X)))
for i in range(len(X)):
    for j in range(len(X)):
        y_approxMatLS[i][j] = y_approxLS[len(X)*i+j]


fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0, antialiased=False)

fig2 = plt.figure()
ax = fig2.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
ax.set_zlim(-1,1)
ax.plot_surface(X, Y, y_approxMatLS, rstride=1, cstride=1, linewidth=0, antialiased=False)

plt.show(block=True)
'''













    
    
    
    