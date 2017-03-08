#/usr/bin/python
# -*- coding: utf-8 -*-
import re
import json

def clean_text(s):
    s_cl = re.sub(r"[^\w\s]", '_', s).lower()
    s_cl = re.sub(r"\s+", '_', s_cl)
    s_cl = re.sub('[_]+', '_', s_cl)
    return s_cl

med_sets = open("medicine_sets.txt", 'r')
generic_meds = open("generic_medlist.txt", 'r')
med_sets_lines = med_sets.readlines()
generic_meds_lines = generic_meds.readlines()

final_sets = {}

for generic_med in generic_meds_lines:
    generic_med = generic_med.strip('\n')

    for med_set in med_sets_lines:
        med_set = med_set.strip('\n')
        asso_med_list = []
        asso_med_list_cl = []
        if generic_med.lower() in med_set.lower():
            generic_med = clean_text(generic_med)
            asso_med_list = med_set.split(",")
            for item in asso_med_list:
                asso_med_list_cl.append(clean_text(item))
            final_sets[generic_med] = asso_med_list_cl
        else:
            continue

print final_sets
print len(final_sets)
med_sets.close()
generic_meds.close()

# write result into json file
with open('gen_med_set.json', 'w') as f:
    json.dump(final_sets, f, indent=2)

# new_list = open("meds/xanax.txt_cl.txt", 'wb')

# effects_list = []
# words = []
# for line in lines:
#   line = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", line).split())
#   print line
#   word = line.split()
#   newline = "_".join(word).lower()
#   print newline
#   effects_list.append(newline)
#   new_list.write(newline+"\n")
# file.close()
# new_list.close()