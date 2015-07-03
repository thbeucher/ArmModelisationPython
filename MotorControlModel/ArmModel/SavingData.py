import numpy as np

#Thomas: to be put in Utils?

class SavingData:
    
    #Sauvegarde et initilisation pour la visualisation du mouvement du bras
    coordElSave = []
    coordHaSave = []
    #Initialisation liste pour sauvegarde
    qsave = []
    dotqsave = []
    ddotqsave = []
    Gammasave = []
    tsave = []
    ub1save = []
    ub2save = []
    ub3save = []
    ut1save = []
    ut2save = []
    ut3save = []
    coordElbowSave = []
    coordHandSave = []
    #Initialisation pour les coordonnees
    xEl = []
    yEl = []
    xHa = []
    yHa = []
        
    def SaveTrajectory(cls, coordEL, coordHA):
        '''
        Saves positions to visualize trajectories
        '''
        cls.coordElSave.append(coordEL)
        cls.coordHaSave.append(coordHA)
    
    def createCoord(cls, a = 1, coordHA = 1, coordEL = 1):
        '''
        This function store the coordinate of the trajectory in order to plot the animation of the trajectory
        '''
        if a == 1:  
            for el in cls.coordElSave:
                cls.xEl.append(el[0])
                cls.yEl.append(el[1])
            for el in cls.coordHaSave:
                cls.xHa.append(el[0])
                cls.yHa.append(el[1])
        else:
            for el in coordEL:
                cls.xEl.append(el[0])
                cls.yEl.append(el[1])
            for el in coordHA:
                cls.xHa.append(el[0])
                cls.yHa.append(el[1])
            
    def saveArmDynamicParameters(cls, q, dotq, ddotq, Gamma_AM, arm):
        '''
        Saves dynamical parameters of the arm
        '''
        #Thomas: renommer la fonction, plus explicite que "Parameters"
        cls.qsave.append((q[0,0],q[1,0]))  
        cls.dotqsave.append((dotq[0,0],dotq[1,0]))
        cls.ddotqsave.append((ddotq[0,0],ddotq[1,0]))
        cls.Gammasave.append((Gamma_AM[0,0],Gamma_AM[1,0]))
        cls.tsave.append(arm.t)
        #Usaveopti(i,:)=U';
        cls.ub1save.append(arm.ub1)
        cls.ub2save.append(arm.ub2)
        cls.ub3save.append(arm.ub3)
        cls.ut1save.append(arm.ut1)
        cls.ut2save.append(arm.ut2)
        cls.ut3save.append(arm.ut3)
        
    SaveTrajectory = classmethod(SaveTrajectory)
    createCoord = classmethod(createCoord)
    saveArmDynamicParameters = classmethod(saveArmDynamicParameters)
    
