'''
Author: Thomas Beucher

Module: MultiCoreComputeTraj

Description: We find here functions which allow to compute trajectory more efficiency using multicore architecture
'''

def computeTraj(JuS, sti, theta):
    '''
    
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
            

        
        
        
        