import numpy as np
import time
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
        phi = self.featureOutput(np.array([inputData]).T)
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
fileSavingStr("RBFN2/Theta", fa.theta)
fileSavingBin("RBFN2/ThetaBIN", fa.theta)'''
       
       
 
        