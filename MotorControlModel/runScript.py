'''
Author: Thomas Beucher

Module: runScript

Description: main script to run what we want in the project
'''
import site
import os

def checkPackages():
    a = site.getsitepackages()
    packageList = os.listdir(a[0])
    packageNeeded = {}
    listOfPackageNeeded = ['pykalman', 'cma', 'cython']
    for el in listOfPackageNeeded:
        packageNeeded[el] = 0
    for el1 in listOfPackageNeeded:
        for el2 in packageList:
            if el1 in el2:
                packageNeeded[el1] = 1
    print(packageNeeded)    
    return packageNeeded

def installMissingPackage(packageList):
    os.system('sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose')
    os.system('clear')

def runAll():
    checkV = True
    while checkV:
        try:
            c = input("is it the first time you run the program? (0 = No, 1 = Yes) : ")
            c = int(c)
            if c == 0 or c == 1:
                checkV = False
        except:
            print("Enter 0 or 1")
    if c == 1:
        packageList = checkPackages()
        installMissingPackage(packageList)
    else:
        pass
    
runAll()


