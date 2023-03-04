# import pandas as pd
import glob
import pprint
import json
import csv
import math
import datetime
import re
from typing import Callable


def get_current_timestamp():
    """return the Unix Epoch as whole seconds"""
    return math.floor(datetime.datetime.now().timestamp())


class calculated_field:
    """
    A csv field that should have the input value converted to a different output value.
    - e.g.: "3" converted to "{TC_VariableName}{TC_VariableName}{TC_VariableName}"
    - Initilized with a regex pattern to define appropriate columns to apply the conversion to.
    - Initiaized with a callable function that recieves a value as input and returns a converted value.
    - Calculated_fields are intended for use by a function or method that parses csv columns and rows
    (See row_parser class)
    """

    def __init__(self, re_pattern_str: str, convert_func: Callable) -> None:
        """
        re_pattern_str : string to be used as a regex pattern
        convert_func : a callable function that returns a string.
        - First argument should be cell_value.
        - All remaining arguments are captured groups from the csv column name
        """
        self.re_pattern_str = re_pattern_str
        self.convert_func: Callable = convert_func
        self.re_result: re.Match[str] | None = None

    def is_definition_match(self, column_name: str) -> bool:
        """Return true if the column name matches the re pattern. False otherwise."""
        self.re_result = re.search(self.re_pattern_str, column_name)
        if self.re_result:
            return True
        return False

    def convert(self, cell_value) -> str | None:
        """Call the conversion function supplied when this class was initiated"""
        if self.re_result:
            args = self.re_result.groups()
            out_str = self.convert_func(cell_value, *args)
            if isinstance(out_str, str):
                return out_str
            else:
                raise TypeError(
                    "convert_func passed to calculated_field must return type str."
                )
        return None


def test_calculated_field():
    calculated_field_list = [
        calculated_field(
            r"(\w*)_num_i_match", lambda n, x: int(n) * ("{" + x + "}")
        ),  # repeat_text_from_col_as_TC_var
        calculated_field(
            r"(\w*)_txt_i_match", lambda t, x: t + "_" + x
        ),  # modify_text_from_col
        calculated_field(
            r"i_won't_be_there", lambda t: "oops! this shouldn't have worked!"
        ),  # match_nothing
    ]

    test_input = [
        ["cube_num_i_match", "not_a_match", "mana_txt_i_match", "target_txt_i_match"],
        [1, 3, "fire", "all"],
        [0, 1, "ice", "single"],
        [5, "never_seen", "tbd", "tbd"],
        ["5", 4, "lightning", 2],
    ]
    column_match_list: list[tuple[bool, int]] = []
    headers = test_input.pop(0)
    for col_name in headers:
        for calc_field in calculated_field_list:
            matching_fields = []
            matching_fields.append(calc_field.is_definition_match(col_name))
            if sum(matching_fields) > 1:
                raise Warning(
                    "There are multiple calculated field matches for this "
                    + "column name. Only one is allowed. "
                    + f"{col_name} : {matching_fields}"
                )
            else:
                try:
                    definition_index = matching_fields.index(True)
                    match_result = (True, definition_index)
                except:
                    match_result = (False, -1)
                finally:
                    column_match_list.append(match_result)
    output_values = [headers]
    for row in test_input:
        i = 0
        new_row: list[str | None] = []
        for cell in row:
            if column_match_list[i][0]:
                new_row.append(
                    calculated_field_list[column_match_list[i][1]].convert(cell)
                )
        output_values.append(new_row)
    pprint.pprint(output_values)


# don't commit yet...
# class row_parser:
#     def __init__(self, col_names:list[str]) -> None:
#         self.convert_list = self._find_calculated_fields(col_names)

#     def define_calculated_fields(self) -> list[calculated_field]:
#         #function for fields ending with "_cubes"
#         def convert_cube_qty(cube_qty: int, mana_row_name: str) -> str:
#             return cube_qty * ("{{" + mana_row_name + "_type}_cube}")

#         calculated_field_list:list[calculated_field] = [
#             calculated_field("(.*)_cubes$", convert_cube_qty)
#         ]
#         return calculated_field_list

#     def _find_calculated_fields(self, col_names:list[str])-> list[Callable]:
#         for name in col_names:
#         convert_list:list[Callable] = []
#         return convert_list
#     def parse_row(self):
#         pass

#     def convert(self, input_value):
#         pass

if __name__ == "__main__":
    # TODO: FIND OUT WHY BROKE :(
    test_calculated_field()
