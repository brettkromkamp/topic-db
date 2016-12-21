"""
DataType enumeration. Part of the StoryTechnologies Builder project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class DataType(Enum):
    string = 1
    number = 2
    timestamp = 3
    boolean = 4
