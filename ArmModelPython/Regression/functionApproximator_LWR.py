import numpy as np


class fa_lwr():
    
    def __init__(self, nbFeature, dim, data = 1, name = 2, xMinMaxE = 3):
        self.nbFeat = nbFeature
        self.dim = dim
        self.centers = {}
        self.thetaLS = np.zeros(self.nbFeat,)
        self.xMinxMax = []
        if xMinMaxE == 3:
            self.rangeValueData(data, name)
        else:
            self.xMinxMax = xMinMaxE
        self.setCentersAndWidths()
    
    ######################################################################################
    ## Fonction d'apprentissage pour la regression                                      ##      
    ######################################################################################
    def train_LS(self, xData, yData):
        #print("feature: ", self.featureOutputLS(xData).shape, "\nOutput: ", np.array(yData).shape)      
        self.thetaLS = np.dot(np.linalg.pinv(np.dot(self.featureOutputLS(xData),np.transpose(self.featureOutputLS(xData)))),np.dot(self.featureOutputLS(xData), np.array(yData)))
    
    def train_LWR(self, xData, yData):
        if self.dim == 4:
            self.theta = np.zeros((self.dim+1,self.nbFeat))
            Ak = np.zeros((self.dim+1,self.dim+1))
            bk = np.zeros((self.dim+1,1))
        elif self.dim == 2:
            ###################################################################################################
            #En dimension 
            self.theta = np.zeros((self.dim+1,self.nbFeat**self.dim))##TEST##
            Ak = np.zeros((self.dim+1,self.dim+1))
            bk = np.zeros((self.dim+1,1))
            ###################################################################################################
        numDataPoints = len(xData)
        
        #----------------------#        
        ## Training Algorithm ##
        #----------------------#
                
        for k in range(self.nbFeat**self.dim):##TEST##
            for i in range(numDataPoints):
                w = self.getWeights(xData[i])
                wTmp = []
                for t in range(self.nbFeat):##TEST##
                    wTmp = np.hstack((wTmp, w[t]))##TEST##
                wkt = float(wTmp[k])##TEST##
                #wk = float(w[k])
                Ak += wkt*np.dot(self.featureOutput(xData[i]), np.transpose(self.featureOutput(xData[i])))##TEST##
                bk += wkt*np.dot(self.featureOutput(xData[i]),yData[i])##TEST##
            self.theta[:,k] = np.dot(np.linalg.pinv(Ak), bk)[:,0]
    
    ######################################################################################
    ## Fonction pour fixer les centres et les sigmas des gaussiennes utilisees          ##      
    ######################################################################################
    def setCentersAndWidths(self):
        centersAxe = {}
        self.widthConstant = 10 / self.nbFeat
        if self.dim == 4:
            centersPP1 = np.linspace((self.xMinxMax[0])[0], (self.xMinxMax[0])[1], self.nbFeat)
            centersPP2 = np.linspace((self.xMinxMax[1])[0], (self.xMinxMax[1])[1], self.nbFeat)
            centersP1 = np.linspace((self.xMinxMax[2])[0], (self.xMinxMax[2])[1], self.nbFeat)
            centersP2 = np.linspace((self.xMinxMax[3])[0], (self.xMinxMax[3])[1], self.nbFeat)
            self.centers[0], self.centers[1], self.centers[2], self.centers[3] = np.meshgrid(centersPP1, centersPP2, centersP1, centersP2)
            self.widths = np.ones(self.nbFeat,) * self.widthConstant
        #################################################
        #En dimension 2
        elif self.dim == 2:
            '''self.centersX = np.linspace(-5,5,self.nbFeat)
            self.centersY = np.linspace(-5,5,self.nbFeat)
            self.centersXt, self.centersYt = np.meshgrid(self.centersX, self.centersY)##TEST##
            self.widths = np.ones(self.nbFeat,) * self.widthConstant
            self.widthst = np.ones((self.nbFeat, self.nbFeat)) * self.widthConstant##TEST##'''
            for i in range(self.dim):
                centersAxe[i] = np.linspace(-5,5,self.nbFeat)
            self.centers[0], self.centers[1] = np.meshgrid(centersAxe[0], centersAxe[1])
        
    
    ######################################################################################
    ## Fonction pour calculer le poids de chaque input par des gaussiennes              ##      
    ######################################################################################    
    def getWeights(self, inputgw):
        if self.dim == 4:
            if np.size(inputgw) == 4:
                W = np.exp(-(np.divide(np.square(inputgw[0] - self.centersPP1), self.widths) 
                             + np.divide(np.square(inputgw[1] - self.centersPP2), self.widths)
                             + np.divide(np.square(inputgw[2] - self.centersP1), self.widths)
                             + np.divide(np.square(inputgw[3] - self.centersP2), self.widths)))
            elif np.size(inputgw) > 4:
                numEvals = ((np.mat(inputgw)).shape)[0]
                el0 = []
                el1 = []
                el2 = []
                el3 = []
                for el in inputgw:
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
            if np.size(inputgw) == 2:
                W = np.exp(-(np.divide(np.square(inputgw[0] - self.centersXt), self.widthst) 
                             + np.divide(np.square(inputgw[1] - self.centersYt), self.widthst)))##TEST##
                
            elif np.size(inputgw) > 2:
                numEvals = ((np.mat(inputgw)).shape)[0]
                el0 = []
                el1 = []
                for el in inputgw:
                    el0.append(el[0])
                    el1.append(el[1])
                inputMat0 = np.array([el0,]*(self.nbFeat**self.dim))##TEST##
                inputMat1 = np.array([el1,]*(self.nbFeat**self.dim))##TEST##
                centersXtTmp = []##TEST##
                centersYtTmp = []##TEST##
                widthsMatTmp = []##TEST##
                for t in range(self.nbFeat):##TEST##
                    centersXtTmp = np.hstack((centersXtTmp, self.centersXt[t]))##TEST##
                    centersYtTmp = np.hstack((centersYtTmp, self.centersYt[t]))##TEST##
                    widthsMatTmp = np.hstack((widthsMatTmp, self.widthst[t]))##TEST##
                centersMat0 = np.array([centersXtTmp,]*numEvals).transpose()##TEST##
                centersMat1 = np.array([centersYtTmp,]*numEvals).transpose()##TEST##
                widthsMat = np.array([widthsMatTmp,]*numEvals).transpose()##TEST##
                W = np.exp(-(np.divide(np.square(inputMat0 - centersMat0), widthsMat)
                             + np.divide(np.square(inputMat1 - centersMat1), widthsMat)))
        ###################################################################################################
        return W
        
    ######################################################################################
    ## Fonction pour calculer la sortie des features selon l'input                      ##      
    ######################################################################################   
    def featureOutput(self, inputfo):   
        if self.dim == 4:
            if np.size(inputfo) == 4:
                phi = np.vstack(([inputfo[0]],[inputfo[1]],[inputfo[2]],[inputfo[3]], [1]))
            elif np.size(inputfo) > 4:
                phi = np.hstack((np.mat(inputfo), np.ones((((np.mat(inputfo)).shape)[0],1))))
        ###################################################################################################
        #En dimension 2
        elif self.dim == 2:
            if np.size(inputfo) == 2:
                phi = np.vstack(([inputfo[0]],[inputfo[1]], [1]))
            elif np.size(inputfo) > 2:
                phi = np.hstack((np.mat(inputfo), np.ones((((np.mat(inputfo)).shape)[0],1)))) 
        ###################################################################################################
        return phi
    
    def featureOutputLS(self, inputfols, a = 1):
        numEvals = ((np.mat(inputfols)).shape)[0]
        ##featureOutputLS en n Dimensions
        dicoInput = {}
        phig = {}
        phigTmp = {}
        for i in range(self.dim):
            dicoInput[i] = []
        for i in range(len(dicoInput)):
            for el in inputfols:
                if a == 2:
                    dicoInput[i].append(el)
                else:
                    dicoInput[i].append(el[0 + i])
        g = 0
        for f in range(self.dim):
            if self.dim == 2:
                for i in range(self.nbFeat):
                    for j in range(self.nbFeat):
                        phig[g] = np.divide(np.square(dicoInput[f] - (self.centers[f])[i][j]), self.widthConstant)
                        g += 1
            elif self.dim == 4:
                for i in range(self.nbFeat):
                    for j in range(self.nbFeat):
                        for k in range(self.nbFeat):
                            for l in range(self.nbFeat):
                                phig[g] = np.divide(np.square(dicoInput[f] - (self.centers[f])[i][j][k][l]), self.widthConstant)
                                g += 1
        for i in range(int(len(phig)/2)):
            phigTmp[i] = phig[i] + phig[i+int(len(phig)/2)]
        for i in range(int(len(phigTmp))):
            phigTmp[i] = np.exp(-phigTmp[i])
        k = 0
        for i in range((self.nbFeat**self.dim)-1):
            if k == 0:
                phit = np.vstack((phigTmp[i], phigTmp[i+1]))
                k += 1
            else:
                phit = np.vstack((phit, phigTmp[i+1]))
        ##featureOutpulLS en 2 dimensions    
        '''el0 = []
        el1 = []
        for el in inputfols:
            el0.append(el[0])
            el1.append(el[1])
        inputMat0 = np.array([el0,]*(self.nbFeat**self.dim))##TEST##
        inputMat1 = np.array([el1,]*(self.nbFeat**self.dim))##TEST##
        centersXtTmp = []##TEST##
        centersYtTmp = []##TEST##
        widthsMatTmp = []##TEST##
        for t in range(self.nbFeat):##TEST##
            centersXtTmp = np.hstack((centersXtTmp, self.centersXt[t]))##TEST##
            centersYtTmp = np.hstack((centersYtTmp, self.centersYt[t]))##TEST##
            widthsMatTmp = np.hstack((widthsMatTmp, self.widthst[t]))##TEST##
        centersMat0 = np.array([centersXtTmp,]*numEvals).transpose()##TEST##
        centersMat1 = np.array([centersYtTmp,]*numEvals).transpose()##TEST##
        widthsMat = np.array([widthsMatTmp,]*numEvals).transpose()##TEST##
        phi = np.exp(-(np.divide(np.square(inputMat0 - centersMat0), widthsMat)
                        + np.divide(np.square(inputMat1 - centersMat1), widthsMat)))'''
        return phit
    
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
    def functionApproximatorOutput(self, inputfao):
        phi = self.featureOutput(inputfao)
        W = self.getWeights(inputfao)
        g = (np.dot(phi, self.theta)).transpose()
        fa_out = np.sum((np.array(W)*np.array(g)), axis=0) / np.sum(np.array(W), axis=0)
        print("phi: ", phi.shape, "Theta: ", self.theta.shape, "W: ", W.shape, "g: ", g.shape, "fa_out: ", fa_out.shape)
        return fa_out
        
    def functionApproximatorOutputLS(self, inputfaols, thethaC, a = 1):
        phi = self.featureOutputLS(inputfaols, 2)
        if a == 1:
            Theta = self.thetaLS
        else:
            Theta = thethaC
        fa_out = np.dot(phi.transpose(), Theta) 
        
        return fa_out
        
        