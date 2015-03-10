import numpy as np

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
        #Sauvegarde position pour visualition trajectoire
        cls.coordElSave.append(coordEL)
        cls.coordHaSave.append(coordHA)
    
    def calculCoord(cls, q, robot):
        coordElbow = (robot.l1*np.cos(q[0,0]), robot.l1*np.sin(q[0,0]))
        coordHand = (robot.l2*np.cos(q[1,0]) + robot.l1*np.cos(q[0,0]), robot.l2*np.sin(q[1,0]) + robot.l1*np.sin(q[0,0]))
        return coordElbow, coordHand
    
    def createCoord(cls):
        for el in cls.coordElSave:
            cls.xEl.append(el[0])
            cls.yEl.append(el[1])
        for el in cls.coordHaSave:
            cls.xHa.append(el[0])
            cls.yHa.append(el[1])
            
    def saveParameters(cls, q, dotq, ddotq, Gamma_AM, arm):
        # Sauvegarde des parametres
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
    calculCoord = classmethod(calculCoord)
    createCoord = classmethod(createCoord)
    saveParameters = classmethod(saveParameters)
    