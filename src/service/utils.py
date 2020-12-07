import re


def get_days_str(days_idx):
    all_days_idx = list(range(7))
    days_names = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
    days_dict = dict(zip(all_days_idx, days_names))
    days_names = [days_dict[i] for i in days_idx]

    return ", ".join(days_names)


def get_days_idx(days_str):
    all_days_idx = list(range(7))
    days_names = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
    days_dict = dict(zip(days_names, all_days_idx))
    days_idx = [days_dict[i] for i in days_str]

    return days_idx


def is_non_negative_int(s):
    # returns true if @s is an integer >= 0
    try:
        if re.search("^\d+$", s) != None:
            return int(s) >= 0
    except ValueError:
        return False
