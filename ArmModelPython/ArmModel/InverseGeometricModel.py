'''
Author: Thomas Beucher

Module: InverseGeometricModel

Description: On retrouve dans ce fichier la fonction resolvant la geometrie inverse d'un bras a deux articulations
'''

import math


def mgi(self, xi, yi, l1, l2):
    '''
    Modele geometrique inverse d'un robot a deux articulations
        
    Entrees:    -xi: abscisse du point effecteur
                -yi: ordonnee du point effecteur
                -l1: longeur du bras
                -l2: longueur de l'avant bras
        
    Sorties:
                -q1: Angle du bras par rapport a l'axe des abscisse
                -q2: Angle de l'avant bras par rapport au bras
    '''
    a = ((xi**2)+(yi**2)-(l1**2)-(l2**2))/(2*l1*l2)
    try:
        q2 = math.acos(a)
        c = l1 + l2*(math.cos(q2))
        d = l2*(math.sin(q2))
        q1 = math.atan2(yi,xi) - math.atan2(d,c)
        return q1, q2
    except ValueError:
        print("Valeur interdite")
        return "None"
    
    
    
    