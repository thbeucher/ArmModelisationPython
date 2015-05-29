'''
Author: Thomas Beucher

Module: testOnKalman

Description: 
'''
from pykalman import KalmanFilter
from pykalman import UnscentedKalmanFilter


def computeTraj(JuS, sti, theta):
    '''
    Computes trajectory more efficiency using multicore architecture
    
    Inputs:     -JuS
                -sti
                -theta
    
    Output:     -JuS
    '''
    i = 0
    for el in sti.posIni:
        Ju = sti.trajGenerator(el[0], el[1], theta)
        JuS[i] = Ju
        i += 1
    return JuS
            
            
def kalmanTest():
    kf = KalmanFilter()
    ukf = UnscentedKalmanFilter()
    
    

        
        
        
        