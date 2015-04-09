'''
Author: Thomas Beucher

Module: InverseGeometricModel

Description: On retrouve dans ce fichier la fonction resolvant la geometrie inverse d'un bras a deux articulations
                ainsi que la fonction resolvant la geometrie directe du bras
'''

import math
import numpy as np

def mgi(xi, yi, l1, l2):
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
    
    
def mgd(q, l1, l2):
    '''
    Modele geometrique directe d'un robot a deux articulations
        
    Entrees:    -q: vecteur contenant q1 et q2
                -l1: longeur du bras
                -l2: longueur de l'avant bras
        
    Sorties:
                -q1: Angle du bras par rapport a l'axe des abscisse
                -q2: Angle de l'avant bras par rapport au bras
    '''
    coordElbow = (l1*np.cos(q[0,0]), l1*np.sin(q[0,0]))
    coordHand = (l2*np.cos(q[1,0] + q[0,0]) + l1*np.cos(q[0,0]), l2*np.sin(q[1,0] + q[0,0]) + l1*np.sin(q[0,0]))
    return coordElbow, coordHand
    
    
def jointStop(q):
    '''
    Cette fonction permet d'appliquer les butees articulaires correspondants au bras humain
    Epaule: -0.6 <= q1 <= 2.6
    Coude: -0.2 <= q2 <= 3.0
    
    Entree:    -q: vecteur position contenant q1 et q2
    
    Sortie:    -q: vecteur position contenant q1 et q2, respectant les butees articulaires
    '''
    if q[0,0] < -0.6:
        q[0,0] = -0.6
    elif q[0,0] > 2.6:
        q[0,0] = 2.6
    if q[1,0] < -0.2:
        q[1,0] = -0.2
    elif q[1,0] > 3.0:
        q[1,0] = 3.0
    return q
    
    
    