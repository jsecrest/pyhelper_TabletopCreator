"""
This version relies on a lot of manual steps based on knowing json of the card I want to modify.
1. Generate card json
a. Create new set and remember set name
b. Create new card in set
c. Modify all fields I may wish to modify with this script
d. Enter set name here and configuration options
"""

# configuration options
set_to_modify = "Spell Test"
mode = "generate_csv"

# import pandas as pd
import glob
import pprint
import json
import csv
import math
import datetime

# blueprint_set_files = glob.glob("data/blueprints/*.json")
component_set_files = glob.glob("data/sets/*.json")
# print(component_set_files)


# blueprints_json_load = dict()
# blueprints = dict()
# for filename in blueprint_set_files:
#     with open(filename) as json_file:
#         blueprints_json_load[filename] = json.load(json_file)

sets_json_load = dict()
for filename in component_set_files:
    with open(filename) as json_file:
        sets_json_load[filename] = json.load(json_file)
    # pprint.pprint(component_set_dict[sf])


def get_current_timestamp():
    """use this to update last_modification_date_unix"""
    return math.floor(datetime.datetime.now().timestamp())


def get_csv_fields_and_samples(
    set_items: dict, verbose: bool = False
) -> list[dict[str, str]]:
    """
    Return a list of dictionarys. Each dictionary entry is an item.
    - An item is (e.g.) a card or a token or a board.
    - Duplicate the item, but flatten the structure to make it CSV friendly.
    - Only keep the "value" and "color" from "data".
    - Example:
        This structure
            {'amount': 3,
             'details': [{'data': {'value': 'pure'}, 'name': 'kickstart_type'},
                         {'data': {'value': 'Mana Bolt'}, 'name': 'title'},
                         {'data': {'color': '#75E67DFF'}, 'name': 'border'}]
        should become
            {'amount': 3,
             'kickstart_type':'pure',
             'title':'Mana Bolt',
             'border': {'color': '#75E67DFF'}
            }
    """
    fields_and_samples: list[dict[str, str]] = []
    for set_item in set_items:
        if verbose:
            print("Original set item:")
            pprint.pprint(set_item)
        flattened_item = {}
        flattened_item["amount"] = set_item["amount"]
        # the following only works if there is only a color or a value. If there are both the color will erase the value.
        for detail in set_item["details"]:
            if "value" in detail["data"].keys():
                flattened_item[detail["name"]] = detail["data"]["value"]
            if "color" in detail["data"].keys():
                flattened_item[detail["name"]] = detail["data"]["color"]
        fields_and_samples.append(flattened_item)
    if verbose:
        print("Converted set item:")
        pprint.pprint(fields_and_samples)
    return fields_and_samples


my_set = dict()
for _, set_dict in sets_json_load.items():
    # print(type(set_dict))
    # pprint.pprint(set_dict)
    print(f"Set name: {set_dict['name']}")
    if set_dict["name"] == set_to_modify:
        print("\t- Set name matches!")

        # extract data from json and restructure it
        my_set["name"] = set_dict["name"]
        my_set["fields_and_samples"] = []
        my_set["fields_and_samples"] = get_csv_fields_and_samples(set_dict["items"])

        # prep to write csv
        csv_filename = f"pyhelper_TabletopCreator/{my_set['name']} - set_from_json_{get_current_timestamp()}.csv"
        csv_columns = list(my_set["fields_and_samples"][0].keys())
        csv_samplerow = list(my_set["fields_and_samples"][0].values())
        # make title the first column
        title_index = csv_columns.index("title")
        csv_columns.insert(0, csv_columns.pop(title_index))
        # then make setname the first column
        csv_columns.insert(0, "setname")
        # make the sample row output match the column changes above
        csv_samplerow.insert(0, csv_samplerow.pop(title_index))
        csv_samplerow.insert(0, my_set["name"])

        with open(csv_filename, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows([csv_columns, csv_samplerow])
        print(f"File written: {csv_filename}")
