__author__ = 'Hao'

import csv

taxa_list_path = "../data/medium list_marine families.csv"
pbdb_data_path = "../data/PBDB_output_all.csv"

# Read into user-defined list of taxa: taxon_no and taxon_name

taxa = {}

with open(taxa_list_path, "r") as f:
    for line in f.readlines():
        try:
            taxa[int(line.split(",")[0].strip())] = {
                "taxon_no": int(line.split(",")[0].strip()),
                "taxon_name": line.split(",")[1].strip(),
                "obs": [],
                "obs_collection": []
            }
        except:
            continue

# print(taxa)

# Open PBDB data stored in a local file

taxa_no_column_names = ["phylum_no", "class_no", "order_no", "family_no",
                        "genus_no", "subgenus_no", "accepted_no"]

with open(pbdb_data_path, "r") as f:

    for row in csv.DictReader(f):
        try:
            paleoloc = None
            try:
                paleoloc = {
                    "lng": float(row["paleolng"]),
                    "lat": float(row["paleolat"])
                }
            except:
                paleoloc = None

            for no in [int(row[x]) for x in taxa_no_column_names]:
                if no in taxa:
                    if int(row["collection_no"]) not in taxa[no]["obs_collection"]:
                        taxa[no]["obs_collection"].append(int(row["collection_no"]))
                    if paleoloc not in taxa[no]["obs"]:
                        taxa[no]["obs"].append(paleoloc)
                    break
        except:
            continue

# taxa = {key: taxa[key] for key in taxa if taxa[key]["obs"]}

# Helper function

def count_common_elements(list1, list2):
    count = 0
    for x in list1:
        for y in list2:
            if x == y:
               count += 1
    return count

# Calculate adjacency list

# print(taxa)
print(len(taxa))
print("Start calculating adjacency list ...")
# exit()
adjacency_list = []
for key in taxa:
    tmp = {
        "from": key,
        "to": key,
        "value": len(taxa[key]["obs_collection"])
    }
    adjacency_list.append(tmp)
    # print(tmp)
    for key2 in taxa:
        if key == key2:
            continue
        tmp = {
            "from": key,
            "to": key2,
            "value": count_common_elements(taxa[key]["obs_collection"], taxa[key2]["obs_collection"])
        }
        adjacency_list.append(tmp)

print("Ready to write file ..")

# Write to output file
with open("../output/output.csv", 'w+') as output:
    output.write('from,to,value')
    for x in adjacency_list:
        if x["value"] != 0:
            output.write("\n" + str(x["from"]) + "," + str(x["to"]) + "," + str(x["value"]))