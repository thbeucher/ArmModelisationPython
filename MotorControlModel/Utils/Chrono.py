#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: OLivier Sigaud

Module: Chrono

Description: Class to display time spent in human format rather than seconds
'''
import time

from GlobalVariables import pathWorkingDirectory, pathDataFolder, cmaesPath

class Chrono:
    
    def __init__(self):
        self.name = "Chrono"
        self.start = time.time()
    
    def stop(self):
        stop = time.time()
        dif = stop - self.start
        difstring = ""
        if dif > 3600:
            heures = int(dif/3600)
            difstring = str(heures) + "h "
            dif = dif - (heures*3600)
        if dif > 60:
            minutes = int(dif/60)
            difstring = difstring + str(minutes) + "mn "
            dif = dif - (minutes*60)
        difstring = difstring + str(int(dif)) + "s"
        dif = dif - int(dif)
        difstring = difstring + str(dif) + "ms"
        print("Temps d'execution:", difstring)
