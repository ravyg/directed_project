# -*- coding: utf-8 -*-
import csv
import re
import os


rootDir = "known_effects/22m_med/meds/"

for dir_, _, files in os.walk(rootDir):
    for fileName in files:
        if fileName.endswith('.csv'): 
            relDir = os.path.relpath(dir_, rootDir)
            relFile = os.path.join(rootDir, fileName)
            print "using : " + fileName
            current_known_effects_file = open(relFile, 'r')
            lines = current_known_effects_file.readlines()
            known_effects_in_vocab = {}
            vocab_known_effects_file = open('vocab_known_effects/22m_meds_nourl/'+fileName, 'wb')
            for line in lines:
                line = line.strip("\n")
                effects_set = open("22m_ph_effects_set_noURL_v1.csv", 'r')
                vocab_effects_ckey = csv.reader(effects_set, delimiter=',')
                for effect in vocab_effects_ckey:
                    #print effect[1]
                    if line == effect[1]:
                        #known_effects_in_vocab[effect[0]] = effect[1]
                        vocab_known_effects_file.write(effect[1] + "," + effect[0] + "\n")
                        print effect[0] + " : " + effect[1] + " => " + line
                effects_set.close()
            vocab_known_effects_file.close()


