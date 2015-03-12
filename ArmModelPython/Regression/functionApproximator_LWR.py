import numpy as np


class fa_lwr():
    
    def __init__(self, nbFeature, data, name, dim):
        self.nbFeat = nbFeature
        self.dim = dim
        self.xMinxMax = []
        if data == False and name == False:
            pass
        else:
            self.rangeValueData(data, name)
        self.setCentersAndWidths()
    
    ######################################################################################
    ## Fonction d'apprentissage pour la regression                                      ##      
    ######################################################################################
    def train_LWR(self, xData, yData):
        if self.dim == 4:
            self.theta = np.zeros((5,self.nbFeat))
            Ak = np.zeros((5,5))
            bk = np.zeros((5,1))
        elif self.dim == 2:
            ###################################################################################################
            #En dimension 2
            self.theta = np.zeros((3,self.nbFeat))
            Ak = np.zeros((3,3))
            bk = np.zeros((3,1))
            ###################################################################################################
        numDataPoints = len(xData)
        
        #----------------------#        
        ## Training Algorithm ##
        #----------------------#
                
        for k in range(self.nbFeat):
            for i in range(numDataPoints):
                w = self.getWeights(xData[i])
                wk = float(w[k])
                Ak += wk*np.dot(self.featureOutput(xData[i]), np.transpose(self.featureOutput(xData[i])))
                bk += wk*np.dot(self.featureOutput(xData[i]),yData[i])
            self.theta[:,k] = np.dot(np.linalg.pinv(Ak), bk)[:,0]
    
    ######################################################################################
    ## Fonction pour fixer les centres et les sigmas des gaussiennes utilisees          ##      
    ######################################################################################
    def setCentersAndWidths(self):
        if self.dim == 4:
            self.centersPP1 = np.linspace((self.xMinxMax[0])[0], (self.xMinxMax[0])[1], self.nbFeat)
            self.centersPP2 = np.linspace((self.xMinxMax[1])[0], (self.xMinxMax[1])[1], self.nbFeat)
            self.centersP1 = np.linspace((self.xMinxMax[2])[0], (self.xMinxMax[2])[1], self.nbFeat)
            self.centersP2 = np.linspace((self.xMinxMax[3])[0], (self.xMinxMax[3])[1], self.nbFeat)
            self.widthConstant = 1 / self.nbFeat / 1
            self.widths = np.ones(self.nbFeat,) * self.widthConstant
        #################################################
        #En dimension 2
        elif self.dim == 2:
            self.centersX = np.linspace(-5,5,self.nbFeat)
            self.centersY = np.linspace(-5,5,self.nbFeat)
            self.widthConstant = 10 / self.nbFeat
            self.widths = np.ones(self.nbFeat,) * self.widthConstant
        #################################################
        '''xmin = -7.0
        xmax = 7.0
        self.centersPP1 = np.linspace(xmin, xmax, self.nbFeat)
        self.centersPP2 = np.linspace(xmin, xmax, self.nbFeat)
        self.centersP1 = np.linspace(xmin, xmax, self.nbFeat)
        self.centersP2 = np.linspace(xmin, xmax, self.nbFeat)
        self.widthConstant = (xmax - xmin) / self.nbFeat / 100
        self.widths = np.ones(self.nbFeat,) * self.widthConstant
        tentersPP1 = np.ones(self.nbFeat,) * self.widthConstant
        print(tentersPP1)'''
    
    ######################################################################################
    ## Fonction pour calculer le poids de chaque input par des gaussiennes              ##      
    ######################################################################################    
    def getWeights(self, input):
        if self.dim == 4:
            if np.size(input) == 4:
                W = np.exp(-(np.divide(np.square(input[0] - self.centersPP1), self.widths) 
                             + np.divide(np.square(input[1] - self.centersPP2), self.widths)
                             + np.divide(np.square(input[2] - self.centersP1), self.widths)
                             + np.divide(np.square(input[3] - self.centersP2), self.widths)))
            elif np.size(input) > 4:
                numEvals = ((np.mat(input)).shape)[0]
                el0 = []
                el1 = []
                el2 = []
                el3 = []
                for el in input:
                    el0.append(el[0])
                    el1.append(el[1])
                    el2.append(el[2])
                    el3.append(el[3])
                inputMat0 = np.array([el0,]*self.nbFeat)
                inputMat1 = np.array([el1,]*self.nbFeat)
                inputMat2 = np.array([el2,]*self.nbFeat)
                inputMat3 = np.array([el3,]*self.nbFeat)
                centersMat0 = np.array([self.centersPP1,]*numEvals).transpose()
                centersMat1 = np.array([self.centersPP2,]*numEvals).transpose()
                centersMat2 = np.array([self.centersP1,]*numEvals).transpose()
                centersMat3 = np.array([self.centersP2,]*numEvals).transpose()
                widthsMat = np.array([self.widths,]*numEvals).transpose() 
                W = np.exp(-(np.divide(np.square(inputMat0 - centersMat0), widthsMat)
                             + np.divide(np.square(inputMat1 - centersMat1), widthsMat)
                             + np.divide(np.square(inputMat2 - centersMat2), widthsMat)
                             + np.divide(np.square(inputMat3 - centersMat3), widthsMat)))
        ###################################################################################################
        #En dimension 2
        elif self.dim == 2:
            if np.size(input) == 2:
                W = np.exp(-(np.divide(np.square(input[0] - self.centersX), self.widths) 
                             + np.divide(np.square(input[1] - self.centersY), self.widths)))
            elif np.size(input) > 2:
                numEvals = ((np.mat(input)).shape)[0]
                el0 = []
                el1 = []
                for el in input:
                    el0.append(el[0])
                    el1.append(el[1])
                inputMat0 = np.array([el0,]*self.nbFeat)
                inputMat1 = np.array([el1,]*self.nbFeat)
                centersMat0 = np.array([self.centersX,]*numEvals).transpose()
                centersMat1 = np.array([self.centersY,]*numEvals).transpose()
                widthsMat = np.array([self.widths,]*numEvals).transpose() 
                W = np.exp(-(np.divide(np.square(inputMat0 - centersMat0), widthsMat)
                             + np.divide(np.square(inputMat1 - centersMat1), widthsMat)))
        ###################################################################################################
        return W
        
    ######################################################################################
    ## Fonction pour calculer la sortie des features selon l'input                      ##      
    ######################################################################################   
    def featureOutput(self, input):   
        if self.dim == 4:
            if np.size(input) == 4:
                phi = np.vstack(([input[0]],[input[1]],[input[2]],[input[3]], [1]))
            elif np.size(input) > 4:
                phi = np.hstack((np.mat(input), np.ones((((np.mat(input)).shape)[0],1))))
        ###################################################################################################
        #En dimension 2
        elif self.dim == 2:
            if np.size(input) == 2:
                phi = np.vstack(([input[0]],[input[1]], [1]))
            elif np.size(input) > 2:
                phi = np.hstack((np.mat(input), np.ones((((np.mat(input)).shape)[0],1)))) 
        ###################################################################################################
        return phi
    
    ######################################################################################
    ## Fonction pour calculer la plage de valeurs des differentes variables             ##      
    ######################################################################################  
    def rangeValueData(self, data, name):
        qq1 = []
        qq2 = []
        q1 = []
        q2 = []
        for el in name:
            #Parcourir les valeurs de qq1 pour connaitre son interval
            qq1.append((((sorted(data[str(el + "_state")], key = lambda col: col[0]))[0])[0], ((sorted(data[str(el + "_state")], key = lambda col: col[0], reverse = True))[0])[0]))
            #Parcourir les valeurs de qq2 pour connaitre son interval
            qq2.append((((sorted(data[str(el + "_state")], key = lambda col: col[1]))[0])[1], ((sorted(data[str(el + "_state")], key = lambda col: col[1], reverse = True))[0])[1]))
            #Parcourir les valeurs de q1 pour connaitre son interval
            q1.append((((sorted(data[str(el + "_state")], key = lambda col: col[2]))[0])[2], ((sorted(data[str(el + "_state")], key = lambda col: col[2], reverse = True))[0])[2]))
            #Parcourir les valeurs de q1 pour connaitre son interval
            q2.append((((sorted(data[str(el + "_state")], key = lambda col: col[3]))[0])[3], ((sorted(data[str(el + "_state")], key = lambda col: col[3], reverse = True))[0])[3]))
        self.xMinxMax.append((((sorted(qq1, key = lambda col: col[0]))[0])[0], ((sorted(qq1, key = lambda col: col[1], reverse = True))[0])[1]))
        self.xMinxMax.append((((sorted(qq2, key = lambda col: col[0]))[0])[0], ((sorted(qq2, key = lambda col: col[1], reverse = True))[0])[1]))
        self.xMinxMax.append((((sorted(q1, key = lambda col: col[0]))[0])[0], ((sorted(q1, key = lambda col: col[1], reverse = True))[0])[1]))
        self.xMinxMax.append((((sorted(q2, key = lambda col: col[0]))[0])[0], ((sorted(q2, key = lambda col: col[1], reverse = True))[0])[1]))
    
    
    ######################################################################################
    ## Fonction pour calculer la sortie selon l'entree souhaitee                        ##      
    ###################################################################################### 
    def functionApproximatorOutput(self, input):
        phi = self.featureOutput(input)
        W = self.getWeights(input)
        g = (np.dot(phi, self.theta)).transpose() #[numFeats x Ns]
        fa_out = np.sum((np.array(W)*np.array(g)), axis=0) / np.sum(np.array(W), axis=0)
        print("phi: ", phi.shape, "Theta: ", self.theta.shape, "W: ", W.shape, "g: ", g.shape, "fa_out: ", fa_out.shape)
        return fa_out
        
        
        