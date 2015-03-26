import numpy as np
import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from FileProcessing.FileSaving import fileSavingBin, fileSavingStr
from FileProcessing.FileReading import FileReading
from Regression.VectorCombinaison import cartesian

class fa_rbfn():
    
    def __init__(self, nbFeature):
        self.nbFeat = nbFeature
        self.title = "rbfn"
        
    def setTrainingData(self, inputData, outputData):
        ##Data should be organize by columns##
        self.inputData = inputData
        self.outputData = outputData
        #Récupération des dimensions d'entrees et de sorties ainsi que le nombre de samples
        self.inputDimension, numberOfInputSamples = np.shape(inputData)
        self.outputDimension, numberOfOutputSamples = np.shape(outputData)
        #Vérification du nombre de samples pour l'entree et la sortie
        assert(numberOfInputSamples == numberOfOutputSamples), "Number of samples not equal for output and input"
        self.numberOfSamples = numberOfInputSamples
        self.theta = np.zeros((self.nbFeat, self.outputDimension))

    ################################################################################################
    #### Fonction permettant de calculer les thetas suivant l'algorithme de regression RBFN ########
    ################################################################################################
    def train_rbfn(self):
        A = np.dot(self.featureOutput(self.inputData.T), self.featureOutput(self.inputData.T).T)
        b = np.dot(self.featureOutput(self.inputData.T), self.outputData.T)
        self.theta = np.dot(np.linalg.pinv(A), b)
       

    ################################################################################################
    ## Fonction permettant de fixer les centres des gaussiennes utilisees et leurs sigma ###########
    ################################################################################################
    def setCentersAndWidths(self):
        #Récupère les minimums et maximum dans les données d'entrées
        minInputData = np.min(self.inputData, axis = 1)
        maxInputData = np.max(self.inputData, axis = 1)
        rangeForEachDim = maxInputData - minInputData
        #Fixe les sigmas
        widthConstant = rangeForEachDim / self.nbFeat
        #créé la matrice diagonales des sigmas pour le calcul de la gaussienne
        self.widths = np.diag(widthConstant)
        self.norma = 1/np.sqrt(((2*np.pi)**self.inputDimension)*np.linalg.det(self.widths)) #coef for gaussian
        linspaceForEachDim = []
        #Fixe le nombre de gaussienne utilisées et les réparties selon chaques dimensions
        for i in range(self.inputDimension):
            linspaceForEachDim.append(np.linspace(minInputData[i], maxInputData[i], self.nbFeat))
        #Permet de récupérer une matrice contenant toutes les combinaisons possibles pour trouver chaque centre
        self.centersInEachDimensions = cartesian(linspaceForEachDim)
    
    ################################################################################################
    ##### Fonction calculant les sorties, selon chaques gaussienne, pour l'entree choisie ##########
    ################################################################################################
    def featureOutput(self, inputData):
        #Si il n'y a qu'un seul échantillon
        if inputData.shape[1] == 1:
            x_u = inputData - self.centersInEachDimensions.T
            x_u_s = np.dot(x_u.T, np.linalg.pinv(self.widths))
            x = x_u_s * (x_u.T)
            xf = np.sum(x, axis = 1)
            phi = self.norma*np.exp(-0.5*xf)
        #Si il y en a plusieurs (echantillons)
        else:
            for i in range(inputData.shape[0]):
                x_u = np.array([inputData[i]]).T - self.centersInEachDimensions.T
                x_u_s = np.dot(x_u.T, np.linalg.pinv(self.widths))
                x = x_u_s * (x_u.T)
                xf = np.sum(x, axis = 1)
                xfe = self.norma*np.exp(-0.5*xf)
                if i == 0:
                    phi = np.array([xfe]).T
                else:
                    phi = np.hstack((phi, np.array([xfe]).T))
        return phi

    ################################################################################################
    ##### Fonction retournant la sortie approximée pour l'entrée donnée et le theta fourni #########
    ################################################################################################
    def functionApproximatorOutput(self, inputData, theta):
        if inputData.shape[1] == 1:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        else:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        return fa_out
       
       
################################################################################################
## TEST 2D                                                                                    ##
################################################################################################
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
nbFeat2 = 3
funApproxDim2 = fa_rbfn(20)
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

plt.show(block=True)'''
        