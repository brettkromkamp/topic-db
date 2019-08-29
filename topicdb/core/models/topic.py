"""
Topic class. Part of the StoryTechnologies project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from typing import List, Optional

from topicdb.core.models.basename import BaseName
from topicdb.core.models.entity import Entity
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence


class Topic(Entity):
    def __init__(
        self,
        identifier: str = "",
        instance_of: str = "topic",
        base_name: str = "Undefined",
        language: Language = Language.ENG,
    ) -> None:
        super().__init__(identifier, instance_of)

        default_base_name = BaseName(base_name, language)

        self.__base_names = [default_base_name]
        self.__occurrences: List[Occurrence] = []
        self.language = language

    @property
    def base_names(self) -> List[BaseName]:
        return self.__base_names

    @property
    def occurrences(self) -> List[Occurrence]:
        return self.__occurrences

    @property
    def first_base_name(self) -> BaseName:
        if len(self.__base_names) > 0:
            result = self.__base_names[0]
        else:
            result = BaseName("Undefined", Language.ENG)
        return result

    def get_base_name(self, identifier: str) -> Optional[BaseName]:
        result = None
        for base_name in self.__base_names:
            if base_name.identifier == identifier:
                result = base_name
                break
        return result

    def add_base_name(self, base_name: BaseName) -> None:
        self.__base_names.append(base_name)

    def add_base_names(self, base_names: List[BaseName]) -> None:
        self.__base_names = [*self.__base_names, *base_names]

    def remove_base_name(self, identifier: str) -> None:
        self.__base_names[:] = [
            x for x in self.__base_names if x.identifier != identifier
        ]

    def clear_base_names(self) -> None:
        del self.__base_names[:]

    def add_occurrence(self, occurrence: Occurrence) -> None:
        occurrence.topic_identifier = self.identifier
        self.__occurrences.append(occurrence)

    def add_occurrences(self, occurrences: List[Occurrence]) -> None:
        for occurrence in occurrences:
            occurrence.topic_identifier = self.identifier
            self.__occurrences.append(occurrence)

    def remove_occurrence(self, identifier: str) -> None:
        self.__occurrences[:] = [
            x for x in self.__occurrences if x.identifier != identifier
        ]

    def get_occurrence(self, identifier: str) -> Optional[Occurrence]:
        result = None
        for occurrence in self.__occurrences:
            if occurrence.identifier == identifier:
                result = occurrence
                break
        return result

    def clear_occurrences(self) -> None:
        del self.__occurrences[:]
