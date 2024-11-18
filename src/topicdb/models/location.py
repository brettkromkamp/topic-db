"""
Location class. Part of the Contextualise (https://contextualise.dev) project.

November 18, 2024
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import re


class Location:
    coordinate_regex = re.compile(
        r"^\s*([-+]?(?:90(?:\.0+)?|(?:[1-8]?\d(?:\.\d+)?)))\s*,\s*([-+]?(?:180(?:\.0+)?|(?:1[0-7]\d(?:\.\d+)?|(?:[1-9]?\d(?:\.\d+)?))))\s*$"
    )

    def __init__(self, identifier: str = "", description: str = "Not provided") -> None:
        self.__identifier = identifier
        self.description = description
        self.__coordinates: str | None = None

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def coordinates(self) -> str | None:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value: str) -> None:
        if not Location.coordinate_regex.match(value):
            raise ValueError("Invalid coordinates")
        self.__coordinates = value
        self.__latitude = value.split(",")[0] if value else ""
        self.__longitude = value.split(",")[1] if value else ""

    @property
    def latitude(self) -> str:
        return self.__latitude

    @property
    def longitude(self) -> str:
        return self.__longitude
