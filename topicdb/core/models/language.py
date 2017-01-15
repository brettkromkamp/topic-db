"""
Language enumeration. Part of the StoryTechnologies Builder project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class Language(Enum):

    # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    # https://en.wikipedia.org/wiki/ISO_639-2

    ENG = 1  # English
    SPA = 2  # Spanish
    DEU = 3  # German
    ITA = 4  # Italian
    FRA = 5  # French
    NLD = 6  # Dutch
    NOB = 7  # Norwegian (Bokmål)
