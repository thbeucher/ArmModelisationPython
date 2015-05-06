'''
Author: Thomas Beucher

Module: RunRegressionRBFN

Description: We find here the function to run rbfn algorithm to create the controller
'''
from Utils.FileReading import FileReading
from Utils.FileSaving import fileSavingBin, fileSavingStr
from Regression.functionApproximator_RBFN import fa_rbfn
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from Utils.ReadSetupFile import ReadSetupFile
from Utils.FunctionsUsefull import learningFieldRBFN, remakeTrajFolder

def saveDataRBFN(nameFile, data):
    fileSavingStr(nameFile, data)
    nameFile += "BIN"
    fileSavingBin(nameFile, data)

####################################################################################################
## runRBFN permet de lancer l'algorithme de regression sur les données de trajectoires du brent ####
####################################################################################################
def runRBFN(calli = 0):
    print("Début de traitement!")
    t0 = time.time()
    fr = FileReading()
    rs = ReadSetupFile()
    nbfeat = rs.numfeats
    #getting all data
    
    #learningFieldRBFN()
    
    state, command = fr.getData(rs.pathFolderTrajectories)
    #change the data (dictionary) into numpy array
    stateAll, commandAll = fr.dicToArray(state), fr.dicToArray(command)
    print("nombre d'echantillons: ", stateAll.shape[0])
    
    fa = fa_rbfn(nbfeat)
    fa.setTrainingData(stateAll.T, commandAll.T)
    fa.setCentersAndWidths()
    fa.train_rbfn()
    
    #remakeTrajFolder()
    
    name = "RBFN2/" + str(nbfeat) + "feats/ThetaX" + str(calli)
    saveDataRBFN(name, fa.theta)
    t1 = time.time()
    print("Fin du traitement! (temps d'execution:", (t1-t0), "s)")
    
def runXRBFN():
    x = 5
    for i in range(x):
        runRBFN(i)
    
def test2DRBFN(nbFeat2):
################################################################################################
## TEST 2D                                                                                    ##
################################################################################################
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    xData = []
    zData = []
    for i in range(len(X)):
        for j in range(len(X)):
            xData.append((X[i][j],Y[i][j]))
            zData.append(Z[i][j])
    funApproxDim2 = fa_rbfn(nbFeat2)
    funApproxDim2.setTrainingData(np.array(xData).T, np.array([zData]))
    funApproxDim2.setCentersAndWidths()
    funApproxDim2.train_rbfn()
    y_approxRBFN = funApproxDim2.functionApproximatorOutput(np.array(xData), funApproxDim2.theta)
    y_approxMatLS = np.zeros((len(X),len(X)))
    for i in range(len(X)):
        for j in range(len(X)):
            y_approxMatLS[i][j] = y_approxRBFN[len(X)*i+j]
    
    
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