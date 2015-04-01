# Cette fonction basé sur la méthode de Newton-Raphson permet
#de déterminer la racine n-ième d'un nbre. err est l' erreur relative
# en cas de non convergence prendre tol grand (exemple  tol=0.5)
# x0 doit être sous la forme d'un réel (exple x0=1.0)

from math import *

def racin(A, n, x0):
    i=0
    x=x0
    tol=10e-8
    if x==0:
        print("Erreur x0 doit être différent de zéro")
    else:
        while (i<3000):
            c=x
            x=x-((x**(n)-A)/(n*x**(n-1)))
            q=x-c
            err=fabs(q/x)
            i=i+1
    if (err <tol):
        print(c, err)
    else:
        print(" le système ne converge pas. Ajuster le compteur i ou jouer sur tol ou sur x0")
    return c
        
def tronquerNB(nb, vir):
    ex = 10**vir
    nb = nb*ex
    nb = int(nb)
    nb = float(nb)
    nb = nb/ex
    return nb