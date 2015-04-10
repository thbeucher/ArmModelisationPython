from numpy import *

# 2 articulations, 1 muscle par articulation, raideur non nulle
class ParametresHogan:
    
    def __init__(self):
        # Couple maximal
        self.__GammaMax = 2 # Valeur arbitraire
        # Raideur
        self.__K = (2*self.__GammaMax)/pi # Valeur arbitraire
        # Initialisation couple Hogan
        self.__Gamma_H = mat([[0],[0]])
    
    
    #GETTER ET SETTER
    def get_gamma_max(self):
        return self.__GammaMax


    def get_k(self):
        return self.__K


    def get_gamma_h(self):
        return self.__Gamma_H


    def set_gamma_max(self, value):
        self.__GammaMax = value


    def set_k(self, value):
        self.__K = value


    def set_gamma_h(self, value):
        self.__Gamma_H = value

    GammaMax = property(get_gamma_max, set_gamma_max, None, None)
    K = property(get_k, set_k, None, None)
    Gamma_H = property(get_gamma_h, set_gamma_h, None, None)