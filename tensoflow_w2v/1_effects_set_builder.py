# -*- coding: utf-8 -*-
import csv
import re
w2v_vocab = open("results/22m_model_ph_noURL_16E16B/model/vocab.txt", 'r')
#  w2v_vocab = open("results/22m_model_ph/model/vocab.txt", 'r')
word_freq = w2v_vocab.readlines()

se_indi_chv = open("se_indi_chv.csv", 'r')
key_effects = csv.reader(se_indi_chv, delimiter=',')

effects_set = {}

for effect in key_effects:
	for vocab in word_freq:
		effect_word = vocab.split(' ')[0]
		if effect[1] == effect_word:
			effects_set[effect_word] = effect[0]
			print effects_set[effect_word]+": "+ effect[1] +" => "+effect_word

w2v_vocab.close()
#with open('22m_ph_effects_set_v1.csv.csv', 'wb') as effects_set_file:
with open('22m_ph_effects_set_noURL_v1.csv', 'wb') as effects_set_file:
    writer = csv.writer(effects_set_file)
    for key, value in effects_set.items():
       writer.writerow([value, key])
