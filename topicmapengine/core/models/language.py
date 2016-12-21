"""
Language enumeration. Part of the StoryTechnologies Builder project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class Language(Enum):

    # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    # https://en.wikipedia.org/wiki/ISO_639-2

    eng = 1  # English
    spa = 2  # Spanish
    deu = 3  # German
    ita = 4  # Italian
    fra = 5  # French
    nld = 6  # Dutch
    nob = 7  # Norwegian (Bokmål)
