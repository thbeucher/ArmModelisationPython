import numpy as np
import time
from FileProcessing.FileSaving import fileSavingBin
from FileProcessing.FileReading import FileReading

class fa_rbfn():
    
    def __init__(self, nbFeature):
        self.nbFeat = nbFeature
        
    def setTrainingData(self, inputData, outputData):
        #Data should be organize by columns
        numberOfInputSamples, self.inputDimension = np.shape(inputData)
        numberOfOutputSamples, self.outputDimension = np.shape(outputData)
        assert(numberOfInputSamples == numberOfOutputSamples, "Number of sample not equal for output and input")
        self.numberOfSamples = numberOfInputSamples
        self.theta = np.zeros((self.nbFeat, self.outputDimension))
        

    def train_rbfn(self, inputData, outputData):
        A = np.dot(self.featureOutput(inputData), self.featureOutput(inputData).transpose())
        b = np.dot(self.featureOutput(inputData), outputData)
        self.theta = np.dot(np.linalg(A), b)
        #self.thetaLS = np.dot(np.linalg.pinv(np.dot(self.featureOutputLS(xData),np.transpose(self.featureOutputLS(xData)))),np.dot(self.featureOutputLS(xData), np.array(yData)))

    def setCentersAndWidths(self, inputData):
        min = np.min(inputData, axis = 0)
        max = np.max(inputData, axis = 0)
        range = max - min
        widthConstant = range / self.nbFeat
        
        print(min, "\n", max, "\n", range, "\n", widthConstant)


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
fa.setTrainingData(stateAll, commandAll)
fa.setCentersAndWidths(stateAll)

       
       
 
        