import os

def getCSVS(providedPath):
    for fileName in os.listdir(providedPath):
     if os.path.isfile(fileName):
        print (fileName)