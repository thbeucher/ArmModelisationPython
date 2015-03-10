import numpy as np


class fa_lwr():
    
    def __init__(self, nbFeature = 10):
        self.nbFeat = nbFeature
        self.theta = np.zeros((5,self.nbFeat))
    
    ######################################################################################
    ## Fonction d'apprentissage pour la regression                                      ##      
    ######################################################################################
    def train_LWR(self, xData, yData):
        self.theta = np.zeros((5,self.nbFeat))
        numDataPoints = np.size(xData)
        print("nbpts: ", numDataPoints)
        print(type(xData[0]))
        print(yData[0])
        
        #----------------------#        
        ## Training Algorithm ##
        #----------------------#
        
        '''Ak = np.zeros((5,5))
        bk = np.zeros((5,1))
                
        for k in range(self.numFeatures):
            for i in range(numDataPoints):
                w = self.getWeights(xData[i])
                wk = float(w[k])
                Ak += wk*np.dot(self.featureOutput(xData[i]), np.transpose(self.featureOutput(xData[i])))
                bk += wk*np.dot(self.featureOutput(xData[i]),yData[i])
                
            self.theta[:,k] = np.dot(np.linalg.pinv(Ak), bk)[:,0]'''
    
    ######################################################################################
    ## Fonction pour fixer les centres et les sigmas des gaussiennes utilisees          ##      
    ######################################################################################
    def setCentersAndWidths(self):
        self.centersPP1 = 0
        self.centersPP2 = 0
        self.centersP1 = 0
        self.centersP2 = 0
        self.widths = 0
    
    ######################################################################################
    ## Fonction pour calculer le poids de chaque input par des gaussiennes              ##      
    ######################################################################################    
    def getWeight(self, input):
        W = np.exp(-(np.divide(np.square(input[0] - self.centersPP1), 2*self.widths**2) 
        + np.divide(np.square(input[1] - self.centersPP2), 2*self.widths**2)
        + np.divide(np.square(input[2] - self.centersPP2), 2*self.widths**2)
        + np.divide(np.square(input[3] - self.centersP1), 2*self.widths**2)))
        return W
        
    ######################################################################################
    ## Fonction pour calculer la sortie des features selon l'input                      ##      
    ######################################################################################   
    def featureOutput(self, input):       
        phi = np.vstack(([input[0]],[input[1]],[input[2]],[input[3]], [1]))
        return phi
        
        
        
        