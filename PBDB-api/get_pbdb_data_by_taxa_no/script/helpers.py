__author__ = 'Hao'

def split(l):
    pass

s = '1,occ,,,1,Australosutura llanoensis,species,349412,,Australosutura llanoensis,,species,349412,Ivorian,,353.8,345.3,Brezinski,1998,1,Arthropoda,18891,Trilobita,19100,Proetida,21062,Brachymetopidae,56732,Australosutura,21084,,,,4,specimens,-98.099998,31,USNM 9047,,,US,Texas,,,1,,"Near San Saba, TX",gp_mid,-65.59,-27.46,101,US,,Chappel Limestone,,,,S. isostichia - crenulata through S. anchoralis - latus,,,,,,,Late Kinderhookian and Osagean,,"""carbonate""",,,,,,,,,,marine indet.,,,,,,,,,,,body'

# print(s.split(","))

import csv

with open('../data/PBDB_output_all.csv') as f:
    # reader = csv.DictReader(f)
    count = 0
    for row in csv.DictReader(f):
        count += 1
        if count == 3:
            break
        print(row)

print("df")