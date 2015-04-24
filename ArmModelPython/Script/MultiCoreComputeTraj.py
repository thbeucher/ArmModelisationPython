'''
Author: Thomas Beucher

Module: MultiCoreComputeTraj

Description: We find here functions which allow to compute trajectory more efficiency using multicore architecture
'''

def serie1(JuS, sti, theta, nbLoop):
    '''
    
    Inputs:     -JuS
                -sti
                -theta
    
    Output:     -JuS
    '''
    i = 0
    for i in range(nbLoop):
        for el in sti.posIni:
            Ju = sti.trajGenerator(el[0], el[1], theta)
            JuS[i] = Ju*(-1)
            i += 1
    return JuS
            
'''for i in range(nbi):
        JuCf = []
        for el in sti.posIni:
        #for el in posi:
            Ju = sti.trajGenerator(el[0], el[1], theta)
            #print(sti.save.coordHaSave[len(sti.save.coordHaSave)-1])
            JuCf.append(Ju)
        Jutmp[i] = JuCf
    s = 0
    for el in Jutmp.values():
        if s == 0:
            juju = np.array(el)
            s += 1
        else:
            juju = np.vstack((juju, el))
    meanJu = np.mean(np.array([juju]).T, axis = 1)'''
        
        
        
        