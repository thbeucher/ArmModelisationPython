

class ParametresRobot():
    
    def __init__(self):
        # Longueurs des segments [m]
        self.__l1 = 0.30
        self.__l2 = 0.35
        # Distances du centre de gravit??? [m]
        self.__d1 = 0.25 # valeur d'origine : 0.025 
        self.__d2 = 0.45 # valeur d'origine : 0.045
        # Masses des segments [kg]
        self.__m1 = 1.4
        self.__m2 = 1.1
        # Inertie des segments [kg.m^2]
        self.__s1 = 0.11
        self.__s2 = 0.16
        # Parametres de la matrice de Masse M
        self.__k1 = self.__d1 + self.__d2 + (self.__m2 * (self.__l1**2))
        self.__k2 = self.__m2 * self.__l1 * self.__s2
        self.__k3 = self.__d2
        # Parametres de la matrice d'amortissement B
        self.__k6 = 0.05
        self.__k7 = 0.025
        self.__k8 = 0.05
        self.__k9 = 0.025
        
        # Les valeurs ci-dessus correspondent a celles de AM
    
    
    #GETTER ET SETTER
    def get_l_1(self):
        return self.__l1


    def get_l_2(self):
        return self.__l2


    def get_d_1(self):
        return self.__d1


    def get_d_2(self):
        return self.__d2


    def get_m_1(self):
        return self.__m1


    def get_m_2(self):
        return self.__m2


    def get_s_1(self):
        return self.__s1


    def get_s_2(self):
        return self.__s2


    def get_k_1(self):
        return self.__k1


    def get_k_2(self):
        return self.__k2


    def get_k_3(self):
        return self.__k3


    def get_k_6(self):
        return self.__k6


    def get_k_7(self):
        return self.__k7


    def get_k_8(self):
        return self.__k8


    def get_k_9(self):
        return self.__k9


    def set_l_1(self, value):
        self.__l1 = value


    def set_l_2(self, value):
        self.__l2 = value


    def set_d_1(self, value):
        self.__d1 = value


    def set_d_2(self, value):
        self.__d2 = value


    def set_m_1(self, value):
        self.__m1 = value


    def set_m_2(self, value):
        self.__m2 = value


    def set_s_1(self, value):
        self.__s1 = value


    def set_s_2(self, value):
        self.__s2 = value


    def set_k_1(self, value):
        self.__k1 = value


    def set_k_2(self, value):
        self.__k2 = value


    def set_k_3(self, value):
        self.__k3 = value


    def set_k_6(self, value):
        self.__k6 = value


    def set_k_7(self, value):
        self.__k7 = value


    def set_k_8(self, value):
        self.__k8 = value


    def set_k_9(self, value):
        self.__k9 = value

    l1 = property(get_l_1, set_l_1, None, None)
    l2 = property(get_l_2, set_l_2, None, None)
    d1 = property(get_d_1, set_d_1, None, None)
    d2 = property(get_d_2, set_d_2, None, None)
    m1 = property(get_m_1, set_m_1, None, None)
    m2 = property(get_m_2, set_m_2, None, None)
    s1 = property(get_s_1, set_s_1, None, None)
    s2 = property(get_s_2, set_s_2, None, None)
    k1 = property(get_k_1, set_k_1, None, None)
    k2 = property(get_k_2, set_k_2, None, None)
    k3 = property(get_k_3, set_k_3, None, None)
    k6 = property(get_k_6, set_k_6, None, None)
    k7 = property(get_k_7, set_k_7, None, None)
    k8 = property(get_k_8, set_k_8, None, None)
    k9 = property(get_k_9, set_k_9, None, None)
        
        