import numpy as np


class fa_lwr():
    
    def __init__(self, nbFeature, data, name):
        self.nbFeat = nbFeature
        self.theta = np.zeros((5,self.nbFeat))
        self.xMinxMax = []
        self.rangeValueData(data, name)
        self.setCentersAndWidths()
    
    ######################################################################################
    ## Fonction d'apprentissage pour la regression                                      ##      
    ######################################################################################
    def train_LWR(self, xData, yData):
        self.theta = np.zeros((5,self.nbFeat))
        numDataPoints = len(xData)
        
        #----------------------#        
        ## Training Algorithm ##
        #----------------------#
        
        Ak = np.zeros((5,5))
        bk = np.zeros((5,1))
                
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
        self.centersPP1 = np.linspace((self.xMinxMax[0])[0], (self.xMinxMax[0])[1], self.nbFeat)
        self.centersPP2 = np.linspace((self.xMinxMax[1])[0], (self.xMinxMax[1])[1], self.nbFeat)
        self.centersP1 = np.linspace((self.xMinxMax[2])[0], (self.xMinxMax[2])[1], self.nbFeat)
        self.centersP2 = np.linspace((self.xMinxMax[3])[0], (self.xMinxMax[3])[1], self.nbFeat)
        self.widthConstant = 1 / self.nbFeat / 1
        self.widths = np.ones(self.nbFeat,) * self.widthConstant
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
        W = np.exp(-(np.divide(np.square(input[0] - self.centersPP1), self.widths) 
        + np.divide(np.square(input[1] - self.centersPP2), self.widths)
        + np.divide(np.square(input[2] - self.centersP1), self.widths)
        + np.divide(np.square(input[3] - self.centersP2), self.widths)))
        return W
        
    ######################################################################################
    ## Fonction pour calculer la sortie des features selon l'input                      ##      
    ######################################################################################   
    def featureOutput(self, input):       
        phi = np.vstack(([input[0]],[input[1]],[input[2]],[input[3]], [1]))
        return phi
    
    ######################################################################################
    ## Fonction pour calculer la plage de valeurs des differentes variables              ##      
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
        
        
        
        