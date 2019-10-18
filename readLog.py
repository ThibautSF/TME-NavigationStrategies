#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import fnmatch as fnm
import matplotlib
import matplotlib.pyplot as plt

arena_width = 600
arena_height = 600
discrete_px = 50

inputFolder = 'log'
outputFolder = 'out'
posKeepedPerSet = 10

durationSuffixFile = '-TrialDurations-qlearning.txt'
qPosSuffixFile = '-Qpos.npy'
qValuesSuffixFile = '-Qvalues.npy'

wantedQValues = ['00002','00072','00000','00070','11101','11171']

def readListPos(lst):
    lstX = list()
    lstY = list()
    for onePos in lst:
        lstX.append(onePos.x())
        lstY.append(onePos.y())
    
    return lstX, lstY

def transformToMatrix(matrix, dct):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if (x,y) in dct:
                matrix[x][y] = dct[(x,y)]
    
    return matrix

def showHeatMap(lstX, lstY):
    global discrete_px
    
    plt.figure()
    plt.hist2d(lstX, lstY, bins=discrete_px, cmap='hot')
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.show()

def saveHeatMap(lstX, lstY, pathfile):
    global discrete_px
    
    plt.figure()
    plt.hist2d(lstX, lstY, bins=discrete_px, cmap='hot')
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.savefig(pathfile)

def heatMap(exp, todo='show'):
    global qPosSuffixFile
    global posKeepedPerSet
    path = inputFolder+'/'+exp+qPosSuffixFile
    positions = np.load(path, allow_pickle=True)
    
    visitedFromBeginX = list()
    visitedFromBeginY = list()
    
    visitedFromEndX = list()
    visitedFromEndY = list()
    
    i = 0
    j = len(positions) - 1
    while i < posKeepedPerSet or j > len(positions) - 1 - posKeepedPerSet:
        posListFromBegin = positions[i]
        posListFromEnd = positions[j]
        
        lstX, lstY = readListPos(posListFromBegin)
        visitedFromBeginX += lstX
        visitedFromBeginY += lstY
        
        lstX, lstY  = readListPos(posListFromEnd)
        visitedFromEndX += lstX
        visitedFromEndY += lstY
        
        i+=1
        j-=1
    
    if todo == 'show':
        showHeatMap(visitedFromBeginX, visitedFromBeginY)
        showHeatMap(visitedFromEndX, visitedFromEndY)
    if todo == 'save':
        pathSave = outputFolder + '/' + exp
        saveHeatMap(visitedFromBeginX, visitedFromBeginY, pathSave+'_begin.png')
        saveHeatMap(visitedFromEndX, visitedFromEndY, pathSave+'_end.png')
    
def qValues(exp, todo='show'):
    global qValuesSuffixFile
    global wantedQValues
    
    path = inputFolder+'/'+exp+qValuesSuffixFile
    qvalues = np.load(path, allow_pickle=True).item()
    
    if todo == 'save':
        pathSave = outputFolder + '/' + exp + '_qvaltolook.txt'
        file = open(pathSave,"w+")
    
    for one_wantedqvalue in wantedQValues:
        s = one_wantedqvalue + " : "
        if one_wantedqvalue in qvalues:
           s += str(qvalues[one_wantedqvalue])
        else:
            s += "null"
        
        s += "\r\n"
        
        if todo == 'show':
            print(s)
        if todo == 'save':
            file.write(s)

def runlength(exp, todo='show'):
    global durationSuffixFile
    
    path = inputFolder+'/'+exp+durationSuffixFile
    times = np.loadtxt(path)
    
    plt.figure()
    plt.plot(times)
    
    if todo == 'show':
        plt.show()
    if todo == 'save':
        pathSave = outputFolder + '/' + exp + '_qlearnTime.png'
        plt.savefig(pathSave)
        
    calcBeginEndDurationInfos(times, todo)

def calcBeginEndDurationInfos(times, todo='show'):
    #print(len(times[0:posKeepedPerSet]))
    #print(len(times[len(times)-posKeepedPerSet:]))
    mn = 'Mean: '+str(np.mean(times[0:posKeepedPerSet]))+'\r\n'
    md = 'Median: '+str(np.median(times[0:posKeepedPerSet]))+'\r\n'
    p1 = '25-percentile: '+str(np.percentile(times[0:posKeepedPerSet], 25))+'\r\n'
    p3 = '75-percentile: '+str(np.percentile(times[0:posKeepedPerSet], 75))+'\r\n'
    
    if todo == 'show':
        print(mn)
        print(md)
        print(p1)
        print(p3)
    if todo == 'save':
        pathout = outputFolder + '/' + exp + '_q8_begin.txt'
        fileOUT = open(pathout, "w+")
        fileOUT.write(mn)
        fileOUT.write(md)
        fileOUT.write(p1)
        fileOUT.write(p3)
    
    mn = 'Mean: '+str(np.mean(times[len(times)-posKeepedPerSet:]))+'\r\n'
    md = 'Median: '+str(np.median(times[len(times)-posKeepedPerSet:]))+'\r\n'
    p1 = '25-percentile: '+str(np.percentile(times[len(times)-posKeepedPerSet:], 25))+'\r\n'
    p3 = '75-percentile: '+str(np.percentile(times[len(times)-posKeepedPerSet:], 75))+'\r\n'
    
    if todo == 'show':
        print(mn)
        print(md)
        print(p1)
        print(p3)
    if todo == 'save':
        pathout = outputFolder + '/' + exp + '_q8_end.txt'
        fileOUT = open(pathout, "w+")
        fileOUT.write(mn)
        fileOUT.write(md)
        fileOUT.write(p1)
        fileOUT.write(p3)

if __name__ == '__main__':
    try:
      os.makedirs(outputFolder)
    except OSError:
        print ("Creation of the directory %s failed" % outputFolder)
    else:
        print ("Successfully created the directory %s" % outputFolder)
      
    onlyfiles = [f for f in os.listdir(inputFolder) if fnm.fnmatch(f, '*'+qPosSuffixFile)]
    
    experiences = []
    for filename in onlyfiles:
        pos = filename.index(qPosSuffixFile)
        experiences.append(filename[0:pos])
    
    print(experiences)
    
    for exp in experiences:
        heatMap(exp, 'save')
        qValues(exp, 'save')
        runlength(exp, 'save')
    
