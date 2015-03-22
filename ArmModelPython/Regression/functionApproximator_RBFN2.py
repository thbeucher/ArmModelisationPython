import numpy as np
import time
from FileProcessing.FileSaving import fileSavingBin
from FileProcessing.FileReading import FileReading

class fa_rbfn():
    
    def __init__(self, nbFeature):
        self.nbFeat = nbFeature
        
    def setTrainingData(self, inputData, outputData):
        #Data should be organize by columns
        self.inputData = inputData
        self.outputData = outputData
        self.inputDimension, numberOfInputSamples = np.shape(inputData)
        self.outputDimension, numberOfOutputSamples = np.shape(outputData)
        assert(numberOfInputSamples == numberOfOutputSamples, "Number of samples not equal for output and input")
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
        centersInEachDimensions = np.zeros((self.inputDimension, self.nbFeat))
        for i in range(self.inputDimension):
            centersInEachDimensions[i,:] = np.linspace(minInputData[i], maxInputData[i], self.nbFeat)
        centersFlat = centersInEachDimensions.flatten()
        centersMesh1, centersMesh2 = np.meshgrid(centersFlat, centersFlat)
        #range = max - min
        #widthConstant = range / self.nbFeat
        
        print(minInputData.shape, "\n", maxInputData.shape, "\ncent:\n ", centersInEachDimensions, "\nflat\n", centersFlat.shape)
        print(centersMesh1.shape)


    def featureOutput(self, inputData):
        pass


    def functionApproximatorOutput(self, inputData):
        pass
       
       
namex = "TestRBFN2/xData"
namez = "TestRBFN2/zData"
fr = FileReading()
stateAll, commandAll = fr.recup_data(0)
print("state: ", stateAll.shape, "command: ", commandAll.shape)

fa = fa_rbfn(3)
fa.setTrainingData(stateAll.T, commandAll.T)
fa.setCentersAndWidths()

       
       
 
        