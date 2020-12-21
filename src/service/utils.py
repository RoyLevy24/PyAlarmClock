"""This module contains utility functions used throughout the project"""

import os
import re
import speech_recognition as sr
import cv2


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
    """
    Retruns an absolute path from a relative path.
    """
    return os.path.join(os.path.dirname(__file__), rel_path)

def check_ratio(num, lower, upper):
    try:
        return lower<=num<=upper
    except Exception:
        return False

def get_num_camera_devices():
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            index += 1
        cap.release()
    return index

def get_num_microphone_devices():
    return len(sr.Microphone.list_microphone_names())