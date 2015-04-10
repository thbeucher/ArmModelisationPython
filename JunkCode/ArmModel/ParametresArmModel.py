from numpy import *
from numpy.linalg import inv

# 2 articulations, 3 muscles par articulation, raideur nulle
class ParametresArmModel:
    
    def __init__(self, __GammaMax):
        # Matrice des moments du bras (Arm Model)
        self.__At = mat([(0.04,-0.04,0,0,0.028,-0.035),(0,0,0.025,-0.025,0.028,-0.035)]) # Valeurs de AM
        #  Vecteurs des tensions musculaires maximales
        self.__fmax = diag([700,382,572,445,159,318]) # Valeurs de AM
        # Activation musculaires 
        self.__ut1=0
        self.__ub1=0
        self.__ut2=0
        self.__ub2=0
        self.__ut3=0
        self.__ub3=0
        # Initialisation couple Arm model
        self.__Gamma_AM = mat([[0.],[0.]])
        # Vitesse articulaire
        self.__dotq0 = mat([[0.],[0.]])
        # Position articulaire
        self.__q0 = mat([[pi/4],[pi/4]])
        # Parametres de la simulation 
        self.__t = 0
        self.__i = 1
        self.__dt = 0.002
        # Les matrices de raideur
        # Matrice de raideur K nulle
        self.__Knulle = mat([(0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0)])
        # Matrice de raideur K petit
        self.__Kp1 = 10.
        self.__Kp2 = 10. 
        self.__KP1 = 10.
        self.__KP2 = 10.
        self.__Kraid = mat([(self.__KP1,self.__KP1,0,0,self.__Kp1,self.__Kp1),(0,0,self.__Kp2,self.__Kp2,self.__KP2,self.__KP2)])   
        # Matrice de raideur K grand
        self.__KP22 = (80*__GammaMax)/pi
        self.__Kp22=(60*__GammaMax)/pi
        self.__KP11=(200*__GammaMax)/pi
        self.__Kp11=(100*__GammaMax)/pi
        self.__Kgrand = mat([(self.__KP11,self.__KP11,0,0,self.__Kp11,self.__Kp11),(0,0,self.__Kp22,self.__Kp22,self.__KP22,self.__KP22)])     
        # Optimisation de Arm model, 2 articulations, 3 muscles par articulation, raideur nulle        
        # Parametres du couple desire   
        # Gain proportionnel
        self.__Kp = 10 # Valeur arbitraire        
        # Gain derive
        self.__Kd = 2*sqrt(self.__Kp)    
        # Initialisation de la position initiale
        self.__q0_i = mat([[0],[0]])    
        #Initialisation des activations musculaires
        self.__U_i = zeros((6,1))
        # Position desiree
        self.__qdes = mat([[pi/4],[pi/4]])
        #Vitesse desiree
        self.__dotqdes = mat([[0],[0]])
    
    #Fonction MCD, MDD et mgd
    def mgd(cls, q, robot):
        Xp = robot.l1*cos(q[0,0]) + robot.l2*cos(q[0,0]+q[1,0])
        Yp = robot.l1*sin(q[0,0]) + robot.l2*sin(q[0,0]+q[1,0])
        
        theta = q[0,0]+q[1,0]
        
        X = mat([[Xp],[Yp],[theta]])
        return X
    
    def MCD(cls,dotq,q,robot):
        dotXp = -robot.l1*(dotq[0,0])*sin(q[0,0])-robot.l2*(dotq[0,0]+dotq[1,0])*sin(q[0,0]+q[1,0])
        dotYp = robot.l1*(dotq[0,0])*cos(q[0,0])+robot.l2*(dotq[0,0]+dotq[1,0])*cos(q[0,0]+q[1,0])
        
        dottheta = (dotq[0,0]+dotq[1,0])
        
        dotX = mat([[dotXp],[dotYp],[dottheta]])
        J = mat([(-robot.l1*sin(q[0,0])-robot.l2*sin(q[0,0]+q[1,0]),-robot.l2*sin(q[0,0]+q[1,0])),(robot.l1*cos(q[0,0])+robot.l2*cos(q[0,0]+q[1,0]),robot.l2*cos(q[0,0]+q[1,0]))])
        return dotX, J
        
    def MDD(cls,Gamma,q,dotq,robot):
        M = mat([(robot.k1+2*robot.k2*cos(q[1,0]),robot.k3+robot.k2*cos(q[1,0])), (robot.k3+robot.k2*cos(q[1,0]),robot.k3)])
        C = transpose(mat([-(2*dotq[0,0]+dotq[1,0])*robot.k2*sin(q[1,0]),dotq[0,0]**2*robot.k2*sin(q[1,0])]))
        B = mat([(robot.k6,robot.k7),(robot.k8,robot.k9)])
        
        M1 = inv(M)
        
        ddotq = M1*(Gamma - C - B*dotq)
        return ddotq
    
    mgd = classmethod(mgd)
    MCD = classmethod(MCD)
    MDD = classmethod(MDD)
    #GETTER ET SETTER
    def get_at(self):
        return self.__At


    def get_fmax(self):
        return self.__fmax


    def get_ut_1(self):
        return self.__ut1


    def get_ub_1(self):
        return self.__ub1


    def get_ut_2(self):
        return self.__ut2


    def get_ub_2(self):
        return self.__ub2


    def get_ut_3(self):
        return self.__ut3


    def get_ub_3(self):
        return self.__ub3


    def get_gamma_am(self):
        return self.__Gamma_AM


    def get_dotq_0(self):
        return self.__dotq0


    def get_q_0(self):
        return self.__q0


    def get_t(self):
        return self.__t


    def get_i(self):
        return self.__i


    def get_dt(self):
        return self.__dt


    def get_knulle(self):
        return self.__Knulle


    def get_kp_1(self):
        return self.__Kp1


    def get_kp_2(self):
        return self.__Kp2


    def get_KP_1(self):
        return self.__KP1


    def get_KP_2(self):
        return self.__KP2


    def get_kraid(self):
        return self.__Kraid


    def get_KP_22(self):
        return self.__KP22


    def get_kp_22(self):
        return self.__Kp22


    def get_KP_11(self):
        return self.__KP11


    def get_kp_11(self):
        return self.__Kp11


    def get_kgrand(self):
        return self.__Kgrand


    def get_kp(self):
        return self.__Kp


    def get_kd(self):
        return self.__Kd


    def get_q_0_i(self):
        return self.__q0_i


    def get_u_i(self):
        return self.__U_i


    def get_qdes(self):
        return self.__qdes


    def get_dotqdes(self):
        return self.__dotqdes


    def set_at(self, value):
        self.__At = value


    def set_fmax(self, value):
        self.__fmax = value


    def set_ut_1(self, value):
        self.__ut1 = value


    def set_ub_1(self, value):
        self.__ub1 = value


    def set_ut_2(self, value):
        self.__ut2 = value


    def set_ub_2(self, value):
        self.__ub2 = value


    def set_ut_3(self, value):
        self.__ut3 = value


    def set_ub_3(self, value):
        self.__ub3 = value


    def set_gamma_am(self, value):
        self.__Gamma_AM = value


    def set_dotq_0(self, value):
        self.__dotq0 = value


    def set_q_0(self, value):
        self.__q0 = value


    def set_t(self, value):
        self.__t = value


    def set_i(self, value):
        self.__i = value


    def set_dt(self, value):
        self.__dt = value


    def set_knulle(self, value):
        self.__Knulle = value


    def set_kp_1(self, value):
        self.__Kp1 = value


    def set_kp_2(self, value):
        self.__Kp2 = value


    def set_KP_1(self, value):
        self.__KP1 = value


    def set_KP_2(self, value):
        self.__KP2 = value


    def set_kraid(self, value):
        self.__Kraid = value


    def set_KP_22(self, value):
        self.__KP22 = value


    def set_kp_22(self, value):
        self.__Kp22 = value


    def set_KP_11(self, value):
        self.__KP11 = value


    def set_kp_11(self, value):
        self.__Kp11 = value


    def set_kgrand(self, value):
        self.__Kgrand = value


    def set_kp(self, value):
        self.__Kp = value


    def set_kd(self, value):
        self.__Kd = value


    def set_q_0_i(self, value):
        self.__q0_i = value


    def set_u_i(self, value):
        self.__U_i = value


    def set_qdes(self, value):
        self.__qdes = value


    def set_dotqdes(self, value):
        self.__dotqdes = value

    At = property(get_at, set_at, None, None)
    fmax = property(get_fmax, set_fmax, None, None)
    ut1 = property(get_ut_1, set_ut_1, None, None)
    ub1 = property(get_ub_1, set_ub_1, None, None)
    ut2 = property(get_ut_2, set_ut_2, None, None)
    ub2 = property(get_ub_2, set_ub_2, None, None)
    ut3 = property(get_ut_3, set_ut_3, None, None)
    ub3 = property(get_ub_3, set_ub_3, None, None)
    Gamma_AM = property(get_gamma_am, set_gamma_am, None, None)
    dotq0 = property(get_dotq_0, set_dotq_0, None, None)
    q0 = property(get_q_0, set_q_0, None, None)
    t = property(get_t, set_t, None, None)
    i = property(get_i, set_i, None, None)
    dt = property(get_dt, set_dt, None, None)
    Knulle = property(get_knulle, set_knulle, None, None)
    Kp1 = property(get_kp_1, set_kp_1, None, None)
    Kp2 = property(get_kp_2, set_kp_2, None, None)
    KP1 = property(get_KP_1, set_KP_1, None, None)
    KP2 = property(get_KP_2, set_KP_2, None, None)
    Kraid = property(get_kraid, set_kraid, None, None)
    KP22 = property(get_KP_22, set_KP_22, None, None)
    Kp22 = property(get_kp_22, set_kp_22, None, None)
    KP11 = property(get_KP_11, set_KP_11, None, None)
    Kp11 = property(get_kp_11, set_kp_11, None, None)
    Kgrand = property(get_kgrand, set_kgrand, None, None)
    Kp = property(get_kp, set_kp, None, None)
    Kd = property(get_kd, set_kd, None, None)
    q0_i = property(get_q_0_i, set_q_0_i, None, None)
    U_i = property(get_u_i, set_u_i, None, None)
    qdes = property(get_qdes, set_qdes, None, None)
    dotqdes = property(get_dotqdes, set_dotqdes, None, None)
        
        
        