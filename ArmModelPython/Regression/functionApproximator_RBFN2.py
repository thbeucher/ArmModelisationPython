import numpy as np
import time
from FileProcessing.FileSaving import fileSavingBin
from FileProcessing.FileReading import FileReading
from Regression.VectorCombinaison import cartesian

class fa_rbfn():
    
    def __init__(self, nbFeature):
        self.nbFeat = nbFeature
        
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
        A = np.dot(self.featureOutput(self.inputData), self.featureOutput(self.inputData).transpose())
        b = np.dot(self.featureOutput(self.inputData), self.outputData)
        self.theta = np.dot(np.linalg(A), b)
        #self.thetaLS = np.dot(np.linalg.pinv(np.dot(self.featureOutputLS(xData),np.transpose(self.featureOutputLS(xData)))),np.dot(self.featureOutputLS(xData), np.array(yData)))

    def setCentersAndWidths(self):
        minInputData = np.min(self.inputData, axis = 1)
        maxInputData = np.max(self.inputData, axis = 1)
        rangeForEachDim = minInputData - maxInputData
        widthConstant = rangeForEachDim / self.nbFeat
        self.widths = np.diag(widthConstant)
        linspaceForEachDim = []
        for i in range(self.inputDimension):
            linspaceForEachDim.append(np.linspace(minInputData[i], maxInputData[i], self.nbFeat))
        self.centersInEachDimensions = cartesian(linspaceForEachDim)


    def featureOutput(self):
        
        pass


    def functionApproximatorOutput(self, inputData):
        pass

       
fr = FileReading()
stateAll, commandAll = fr.recup_data(0)
print("state: ", stateAll.shape, "command: ", commandAll.shape)

fa = fa_rbfn(3)
fa.setTrainingData(stateAll.T, commandAll.T)
fa.setCentersAndWidths()

       
       
 
        