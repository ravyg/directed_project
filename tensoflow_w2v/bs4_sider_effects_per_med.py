from bs4 import BeautifulSoup
import requests
import re
import csv

# output path.
dirpath = "known_effects/22m_med/"

# Building known effects list.
with open (dirpath+"url_medlist.csv", "r") as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    url = row[0]
    med = row[1]

    # Scrap the data.
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    tables = soup.findChildren('table')
    my_table = tables[0]
    rows = my_table.findChildren(['th', 'tr'])
    print "*******Building Side Effects: "+med+"*******"
    side_effects = []
    indications = []
    for row in rows:
      cells = row.findChildren("a", {"href" : re.compile("^/se/C")})
      for cell in cells:
        if cell.text != None:
          value = cell.text
          word = value.split()
          value = "_".join(word).lower()
          side_effects.append(value)

    se_file  = open(dirpath+"meds/"+med+"_se.csv", 'w')
    for item in side_effects:
      se_file.write("%s\n" % item)
    se_file.close
    
          
    print "*******Building Indications: "+med+"*******"
    my_table = tables[1]
    rows = my_table.findChildren(['th', 'tr'])
    for row in rows:
      cells = row.findChildren("a", {"href" : re.compile("^/se/C")})
      for cell in cells:
        if cell.text != None:
          value = cell.text
          word = value.split()
          value = "_".join(word).lower()
          indications.append(value)

    in_file  = open(dirpath+"meds/"+med+"_in.csv", 'wb')
    for item in indications:
      in_file.write("%s\n" % item)
    in_file.close

