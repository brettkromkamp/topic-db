"""
Language enumeration. Part of the Contextualise (https://contextualise.dev) project.

June 12, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
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

    def __str__(self):
        return self.name
