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
        #Data should be organize by columns
        self.inputData = inputData
        self.outputData = outputData
        self.inputDimension, numberOfInputSamples = np.shape(inputData)
        self.outputDimension, numberOfOutputSamples = np.shape(outputData)
        assert(numberOfInputSamples == numberOfOutputSamples), "Number of samples not equal for output and input"
        self.numberOfSamples = numberOfInputSamples
        self.theta = np.zeros((self.nbFeat, self.outputDimension))

    def train_rbfn(self):
        A = np.dot(self.featureOutput(self.inputData.T), self.featureOutput(self.inputData.T).T)
        b = np.dot(self.featureOutput(self.inputData.T), self.outputData.T)
        self.theta = np.dot(np.linalg.pinv(A), b)
        #self.thetaLS = np.dot(np.linalg.pinv(np.dot(self.featureOutputLS(xData),np.transpose(self.featureOutputLS(xData)))),np.dot(self.featureOutputLS(xData), np.array(yData)))

    def setCentersAndWidths(self):
        minInputData = np.min(self.inputData, axis = 1)
        maxInputData = np.max(self.inputData, axis = 1)
        rangeForEachDim = maxInputData - minInputData
        widthConstant = rangeForEachDim / self.nbFeat
        self.widths = np.diag(widthConstant)
        self.norma = 1/np.sqrt(((2*np.pi)**self.inputDimension)*np.linalg.det(self.widths)) #coef for gaussian
        linspaceForEachDim = []
        for i in range(self.inputDimension):
            linspaceForEachDim.append(np.linspace(minInputData[i], maxInputData[i], self.nbFeat))
        self.centersInEachDimensions = cartesian(linspaceForEachDim)

    def featureOutput(self, inputData):
        if inputData.shape[1] == 1:
            x_u = inputData - self.centersInEachDimensions.T
            x_u_s = np.dot(x_u.T, np.linalg.pinv(self.widths))
            x = x_u_s * (x_u.T)
            xf = np.sum(x, axis = 1)
            phi = self.norma*np.exp(-0.5*xf)
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


    def functionApproximatorOutput(self, inputData, theta):
        if inputData.shape[1] == 1:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        else:
            phi = self.featureOutput(inputData)
            fa_out = np.dot(phi.T, theta) 
        return fa_out

       
'''fr = FileReading()
stateAll, commandAll = fr.recup_data(0)
print("state: ", stateAll.shape, "command: ", commandAll.shape)

fa = fa_rbfn(3)
fa.setTrainingData(stateAll.T, commandAll.T)
fa.setCentersAndWidths()
fa.train_rbfn()
print(fa.theta.shape)
fileSavingStr("RBFN2/3feats/Theta", fa.theta)
fileSavingBin("RBFN2/3feats/ThetaBIN", fa.theta)'''
       
       
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
        