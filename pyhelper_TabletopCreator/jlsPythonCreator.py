# import pandas as pd
import glob
import pprint
import json

blueprint_set_files = glob.glob("data/blueprints/*.json")
component_set_files = glob.glob("data/sets/*.json")
# print(component_set_files)

bluepirnts = dict()
sets = dict()

for filename in blueprint_set_files:
    with open(filename) as json_file:
        master_dict['blueprints'][filename] = json.load(json_file)

for filename in component_set_files:
    with open(filename) as json_file:
        component_set_dict[filename] = json.load(json_file)
    # pprint.pprint(component_set_dict[sf])


for set_name, set_dict in component_set_dict.items():
    # print(type(set_dict))
    # pprint.pprint(set_dict)
    print(set_dict['name'])

