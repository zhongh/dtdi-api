__author__ = 'zhongh3@rpi.edu'

import requests

###################################################
# Instructions:
#   - Enter the variable values below
#   - At least 1 base name is NEEDED. For multiple base names, separate them with a comma, e.g.
#         "Animalia,Plantae"
#   - max and min ma ages are optional
#   - interval can be defined instead of max and min ages, such as "Cambrian" or "Cambrian,Permian";
#     must NOT have max_ma or min_ma at the same time
#   - enter the desired taxonomy level where co-occurrences are considered, say, "family", "genus"
#   - enter your preferred output file prefix, for example, if you entered "RPI", then
#       the output file name will be "RPI_by_family_from_XXXma_to_YYYma.csv" where XXX and YYY are the
#       max and min ma ages for your convenience at your convenience. If you don't enter a prefix, it will just be
#       "Primates_by_family_from_XXXma_to_YYYma.csv"
#   - run the program by entering:
#
#       python3 get_pbdb_data.py
#
#     then you can find the result file in the same folder!
#
# Now Enter custom variable values:
list_or_matrix = "matrix"         # Required*** options: "list" | "matrix" | "both"
base_name = "Primates"          # Required***
max_ma = ""                    # Optional
min_ma = ""                    # Optional
interval = ""           # Optional, e.g. "Cambrian" or "Cambrian,Permian"; must NOT have max_ma or min_ma at the same time
level = "family"                # Required***
output_file_prefix = ""     # Optional
#
###################################################
# Do not change the codes below.
###################################################

url = "https://paleobiodb.org/data1.2/occs/list.csv"

if base_name:
    url += "?base_name=" + base_name

if interval:
    if not max_ma and not min_ma:
        url += "&interval=" + interval
    else:
        # print("ERROR: Can't have period name and max/min age at the same time! Please adjust your input and re-run the program")
        exit("INPUT ERROR: Input should only have either period name and max/min age at the same time.")
else:
    if max_ma:
        url += "&max_ma=" + max_ma
    if min_ma:
        url += "&min_ma=" + min_ma



url += "&show=full"

# 1. Request the url with stream=True and load the results by lines

print("Requesting url ... (" + str(url) + ")")
r = requests.get(url, stream=True)

print("Url request successful, loading occurrences ... ", end="")

count = 0
variable_names = []
occurrences = []

for line in r.iter_lines():

    count += 1

    if count == 1:
        variable_names = line.decode("utf-8")[1:-1].split('","')
        continue
    else:
        list = str(line, "utf-8")[1:-1].split('","')

        if list[0] == "":
            continue

        occurrence = dict(zip(variable_names, list))

        tmp = {}
        if level in occurrence and occurrence[level]:
            # if occurrence["paleolng"] and occurrence["paleolat"]:
            if occurrence["collection_no"]:
                tmp["taxonomy"] = occurrence[level]
                # tmp["paleoloc"] = {
                #     "lng": float(occurrence["paleolng"]),
                #     "lat": float(occurrence["paleolat"])
                # }
                tmp["collection_no"] = str(occurrence["collection_no"])
                # print(tmp)
                # print(tmp['taxonomy'])
                occurrences.append(tmp)
                continue
        else:
            continue

print("Success!")
# print(occurrences)

# 2. Categorizing occurrences into user's desired level of taxonomies

print("Categorizing occurrences into customized level of taxonomies ... ", end="")
occurrences_by_taxonomies = {}

for occurrence in occurrences:
    if occurrence['taxonomy'] not in occurrences_by_taxonomies:
        occurrences_by_taxonomies[occurrence['taxonomy']] = [str(occurrence["collection_no"])]
    elif occurrence['collection_no'] not in occurrences_by_taxonomies[occurrence['taxonomy']]:
        occurrences_by_taxonomies[occurrence['taxonomy']].append(str(occurrence['collection_no']))
    else:
        continue

print("Success!")
# print(occurrences_by_taxonomies)

########################################
# Helper function
def count_common_elements(list1, list2):
    count = 0
    for x in list1:
        for y in list2:
            if x == y:
               count += 1
    return count
#
########################################

############################################################################################
# Formatting output file name (suffices "_list.csv" and/or "_matrix.csv" will be added later
output_file = output_file_prefix + "_" * (len(output_file_prefix) > 0) \
            + str(base_name) * 0 + "_" * (len(base_name) > 0) * 0 \
            + "by_" + str(level)

if interval:
    if len(interval.split(",")) == 2:
        max_interval = interval.split(",")[0]
        min_interval = interval.split(",")[1]
        output_file += "_from_" + str(max_interval) + "_to_" + str(min_interval) + ".csv"
    else:
        output_file += "_from_" + str(interval)
else:
    output_file += "_from_" + str(max_ma) + "ma_to_" + str(min_ma) + "ma"
#
#######################################################################

#######################################################################
# 3.1 Output Option: List:
if list_or_matrix == "list" or list_or_matrix == "both":
    print("Adjacency list output option enabled.")
    print("    Calculating adjacency list (This might take a while) ... ", end="")
    adjacency_list = []
    for key in occurrences_by_taxonomies:
        tmp = {
            "from": key,
            "to": key,
            "value": len(occurrences_by_taxonomies[key])
        }
        adjacency_list.append(tmp)
        for key2 in occurrences_by_taxonomies:
            if key == key2:
                continue
            tmp = {
                "from": key,
                "to": key2,
                "value": count_common_elements(occurrences_by_taxonomies[key], occurrences_by_taxonomies[key2])
            }
            adjacency_list.append(tmp)
    print("Success!")
    output_file_list = output_file + "_list.csv"
    print("    Writing to adjacency list to output file: " + str(output_file_list))
    with open(output_file_list, 'w+') as output:
        output.write('from,to,value')
        for x in adjacency_list:
            if x["value"] != 0:
                output.write("\n" + str(x["from"]) + "," + str(x["to"]) + "," + str(x["value"]))
#
#######################################################################

#######################################################################
# 3.2 Output Option: Matrix
if list_or_matrix == "matrix" or list_or_matrix == "both":
    print("Adjacency matrix output option enabled.")
    print("    Calculating adjacency matrix (This might take a while) ... ", end="")
    adjacency_matrix = {}
    for key in occurrences_by_taxonomies:
        adjacency_matrix[key] = {}
        adjacency_matrix[key][key] = len(occurrences_by_taxonomies[key])
        for key2 in occurrences_by_taxonomies:
            if key == key2:
                continue
            adjacency_matrix[key][key2] = count_common_elements(occurrences_by_taxonomies[key], occurrences_by_taxonomies[key2])

    print("Success!")
    output_file_matrix = output_file + "_matrix.csv"
    print("    Writing adjacency matrix to output file: " + str(output_file_matrix))
    with open(output_file_matrix, 'w+') as output:
        sorted_taxonomies = sorted(adjacency_matrix)
        for tax in sorted_taxonomies:
            output.write("," + str(tax))
        for tax in sorted_taxonomies:
            output.write("\n" + tax)
            for tax2 in sorted_taxonomies:
                output.write("," + str(adjacency_matrix[tax][tax2]))
#
#######################################################################
print("DONE")