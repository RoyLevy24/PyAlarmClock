# This module contains utility functions for use throughout the project

import re
import os

def get_days_str(days_idx):
    """
    Returns a string separated by commas represanting the days in @days_idx
    """
    all_days_idx = list(range(7))
    days_names = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
    days_dict = dict(zip(all_days_idx, days_names))
    days_names = [days_dict[i] for i in days_idx]

    return ", ".join(days_names)


def is_positive_int(s):
    """Returns true if @s is an integer > 0 ."""
    try:
        if re.search("^\d+$", s) != None:
            return int(s) > 0
    except ValueError:
        return False


def get_abs_path(rel_path):
    return os.path.join(os.path.dirname(__file__), rel_path)
