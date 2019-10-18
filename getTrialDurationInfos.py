#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import fnmatch as fnm

inputFolder = 'log'
outputFolder = 'out'

durationSuffixFile = '-TrialDurations-randomPersist.txt'

if __name__ == '__main__':
    onlyfiles = [f for f in os.listdir(inputFolder) if fnm.fnmatch(f, '*'+durationSuffixFile)]
    
    experiences = []
    for filename in onlyfiles:
        pos = filename.index(durationSuffixFile)
        experiences.append(filename[0:pos])
    
    for exp in experiences:
        pathin = inputFolder+'/'+exp+durationSuffixFile
        pathout = outputFolder+'/'+exp+'_q2.txt'
        fileOUT = open(pathout, "w+")
        
        times = np.loadtxt(pathin)
        
        fileOUT.write('Mean: '+str(np.mean(times)) + '\r\n')
        fileOUT.write('Median: '+str(np.median(times)) + '\r\n')
        fileOUT.write('25-percentile: '+str(np.percentile(times, 25)) + '\r\n')
        fileOUT.write('75-percentile: '+str(np.percentile(times, 75)) + '\r\n')

