__author__ = 'Hao Zhong'

import requests

# This API uses PBDB Data Service 1.2 v1 (https://paleobiodb.org/data1.2/) to access fossil occurrence data.
#
# The data is accessed by URLs that look like:
#       https://paleobiodb.org/data1.2/occs/list.csv?base_name=Animalia&max_ma=300&min_ma=50&show=full,classext
#
# Such an URL takes in parameter values (e.g. "base_name=Animalia" and "max_ma=300") and is able to return a requested
# subset of fossil occurrence data. Please visit https://paleobiodb.org/classic/displayDownloadGenerator where you can
# interactively set up parameters, download data, and observe how the URLs vary and work for different settings.
#
# Note that the last variable in the sample URL above is "show=full,classext". Using "show=full" will include all output
# blocks whose names are boldfaced at the bottom of https://paleobiodb.org/classic/displayDownloadGenerator. However,
# it won't include the classification ext., namely the taxonomy identifier. To do so, we use "show=full,classext".
# Other output options can also be added due to further needs. Please keep exploring the download generator for details.
#
# Instructions:
#   - Enter the variable values below
#   - Either base_name or max_ma and min_ma needs to be specified for the URL to work here.
#   - For multiple base names, separate them with a comma, e.g. "Animalia,Plantae"
#   - max and min ma ages are optional if base_name is specified
#   - interval can be defined instead of max and min ages, such as "Cambrian" or "Cambrian,Permian";
#     must NOT have max_ma or min_ma at the same time
#   - Enter the desired taxonomy level where co-occurrences are considered, say, "family", "genus"
#   - Enter your preferred output file prefix. Otherwise, the name of output file will be standard and only possibly
#     contain parameter information, such as "Primates_by_family_from_XXXma_to_YYYma.csv"
#   - Run the program by entering:
#
#       python3 get_pbdb_data_locality_age.py
#
#     then you can find the result file in the same folder!
#
# Now Enter custom variable values:
table_or_json = "table"         # Required*** options: "table" | "json" | "both"
base_name = ""          # Required***
max_ma = "100"                    # Optional
min_ma = "90"                    # Optional
interval = ""           # Optional, e.g. "Cambrian" or "Cambrian,Permian"; must NOT have max_ma or min_ma at the same time
level = "family"                # Required***
output_file_prefix = ""     # Optional
#
###################################################
# Do not change the codes below.
###################################################

url = "https://paleobiodb.org/data1.2/occs/list.csv?"

url_parameters = []

if base_name:
    url_parameters.append("base_name=" + base_name)
    # url += "base_name=" + base_name

if interval:
    if not max_ma and not min_ma:
        url_parameters.append("interval=" + interval)
        # url += "&interval=" + interval
    else:
        # print("ERROR: Can't have period name and max/min age at the same time! Please adjust your input and re-run the program")
        exit("INPUT ERROR: Input should only have either period name and max/min age at the same time.")
else:
    if max_ma:
        url_parameters.append("max_ma=" + max_ma)
        # url += "&max_ma=" + max_ma
    if min_ma:
        url_parameters.append("min_ma=" + min_ma)
        # url += "&min_ma=" + min_ma

url += "&".join(url_parameters) + "&show=full,classext"

# 1. Request the url with stream=True and load the results by lines

print("Requesting url ... (" + str(url) + ")")
r = requests.get(url, stream=True)
# In certain environments, the request above might not work due to verification issues. Try adding option "verify=False"

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
            if occurrence["paleolng"] and occurrence["paleolat"] and \
                occurrence["lng"] and occurrence["lat"] and \
                occurrence["max_ma"] and occurrence["min_ma"]:
                # Added:
                tmp["base_name"] = base_name
                tmp["min_ma"] = occurrence["min_ma"]
                tmp["max_ma"] = occurrence["max_ma"]
                tmp["loc"] = {
                    "lng": float(occurrence["lng"]),
                    "lat": float(occurrence["lat"])
                }
                tmp["geoplate"] = occurrence["geoplate"]
                tmp["taxon_environment"] = occurrence["taxon_environment"]
                tmp["environment_basis"] = occurrence["environment_basis"]
                tmp["motility"] = occurrence["motility"]
                tmp["life_habit"] = occurrence["life_habit"]
                tmp["vision"] = occurrence["vision"]
                tmp["diet"] = occurrence["diet"]
                tmp["reproduction"] = occurrence["reproduction"]
                tmp["ontogeny"] = occurrence["ontogeny"]
                # End adding
                tmp["taxonomy"] = occurrence[level]
                tmp["paleoloc"] = {
                    "lng": float(occurrence["paleolng"]),
                    "lat": float(occurrence["paleolat"])
                }
                # print(tmp)
                # print(tmp['taxonomy'])
                occurrences.append(tmp)
                continue
        else:
            continue

print("Success!")
# print(occurrences)
############################################################################################
# Formatting output file name
output_file = output_file_prefix + "_" * (len(output_file_prefix) > 0) \
            + str(base_name) * 0 + "_" * (len(base_name) > 0) * 0 \
            + "localities_age_by_" + str(level)

if interval:
    if len(interval.split(",")) == 2:
        max_interval = interval.split(",")[0]
        min_interval = interval.split(",")[1]
        output_file += "_from_" + str(max_interval) + "_to_" + str(min_interval)
    else:
        output_file += "_from_" + str(interval)
else:
    output_file += "_from_" + str(max_ma) + "ma_to_" + str(min_ma) + "ma"
#
#######################################################################

#######################################################################
# 3.1 Output Option: Table:
if table_or_json == "table" or table_or_json == "both":
    print("Tabular output option enabled.")
    output_file_tabular = output_file + ".csv"
    print("    Writing table to output file: " + str(output_file_tabular))
    with open(output_file_tabular, 'w+') as output:
        output.write('base_name,taxonomy,min_ma,max_ma,lng,lat,paleolng,paleolat,geoplate' +
                     ',taxon_environment,environment_basis,motility,life_habit' +
                     ',vision,diet,reproduction,ontogeny')
        for x in occurrences:
            output.write("\n" + str(x["base_name"]) + "," + str(x["taxonomy"]) +
                         "," + str(x["min_ma"]) + "," + str(x["max_ma"]) +
                         "," + str(x["loc"]["lng"]) + "," + str(x["loc"]["lat"]) +
                         "," + str(x["paleoloc"]["lng"]) + "," + str(x["paleoloc"]["lat"]) +
                         "," + str(x["geoplate"]) +
                         "," + str(x["taxon_environment"]) +
                         "," + str(x["environment_basis"]) +
                         "," + str(x["motility"]) +
                         "," + str(x["life_habit"]) +
                         "," + str(x["vision"]) +
                         "," + str(x["diet"]) +
                         "," + str(x["reproduction"]) +
                         "," + str(x["ontogeny"]))
#
#######################################################################

#######################################################################
# 3.2 Output Option: JSON (to be completed; may not be needed)

print("DONE")