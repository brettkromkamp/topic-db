"""
Temporal class. Part of the Contextualise (https://contextualise.dev) project.

November 18, 2024
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import re

from .temporaltype import TemporalType


class Temporal:
    date_regex = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")  # Regex pattern for yyyy-mm-dd dates

    def __init__(
        self, identifier: str = "", type: TemporalType = TemporalType.EVENT, description: str = "Not provided"
    ) -> None:
        self.__identifier = identifier
        self.__type = type
        self.description = description
        self.media_url = ""
        self.__start_date = ""
        self.__end_date: str | None = None  # TODO: Include logic to check that the end date is always greater than the start date

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def type_(self) -> TemporalType:
        return self.__type

    @type_.setter
    def type_(self, value: TemporalType) -> None:
        self.__type = value

    @property
    def start_date(self) -> str:
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str) -> None:
        if not Temporal.date_regex.match(value):
            raise ValueError("Invalid date")
        self.__start_date = value

    @property
    def end_date(self) -> str | None:
        return self.__end_date

    @end_date.setter
    def end_date(self, value: str) -> None:
        if self.__type is TemporalType.EVENT:
            raise ValueError("Temporal event cannot have an end date")
        if not Temporal.date_regex.match(value):
            raise ValueError("Invalid date")
        self.__end_date = value
