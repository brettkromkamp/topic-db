"""
Topic class. Part of the Contextualise (https://contextualise.dev) project.

June 12, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

from topicdb.models.basename import BaseName
from topicdb.models.entity import Entity
from topicdb.models.language import Language
from topicdb.models.occurrence import Occurrence

UNIVERSAL_SCOPE = "*"


class Topic(Entity):
    def __init__(
        self,
        identifier: str = "",
        instance_of: str = "topic",
        name: str = "Undefined",
        # Universal scope is "*". What's more, 'scope' in this context is referring to the scope of the topic's
        # base name objects. Topics, as such, do not have scope.
        scope: str = UNIVERSAL_SCOPE,
        language: Language = Language.ENG,
    ) -> None:
        super().__init__(identifier, instance_of)

        default_base_name = BaseName(name, scope, language)

        self.__base_names = [default_base_name]
        self.__occurrences: list[Occurrence] = []
        self.language = language

    @property
    def base_names(self) -> list[BaseName]:
        return self.__base_names

    @property
    def occurrences(self) -> list[Occurrence]:
        return self.__occurrences

    @property
    def first_base_name(self) -> BaseName:
        if len(self.__base_names) > 0:
            result = self.__base_names[0]
        else:
            result = BaseName("Undefined", UNIVERSAL_SCOPE, Language.ENG)
        return result

    def get_base_name(self, identifier: str) -> BaseName | None:
        result = None
        for base_name in self.__base_names:
            if base_name.identifier == identifier:
                result = base_name
                break
        return result

    def get_base_name_by_scope(self, scope: str) -> BaseName | None:
        result = None
        for base_name in self.__base_names:
            if base_name.scope == scope:
                result = base_name
                break
        return result

    def add_base_name(self, base_name: BaseName) -> None:
        self.__base_names.append(base_name)

    def add_base_names(self, base_names: list[BaseName]) -> None:
        self.__base_names = [*self.__base_names, *base_names]

    def remove_base_name(self, identifier: str) -> None:
        self.__base_names[:] = [x for x in self.__base_names if x.identifier != identifier]

    def clear_base_names(self) -> None:
        del self.__base_names[:]

    def add_occurrence(self, occurrence: Occurrence) -> None:
        occurrence.topic_identifier = self.identifier
        self.__occurrences.append(occurrence)

    def add_occurrences(self, occurrences: list[Occurrence]) -> None:
        for occurrence in occurrences:
            occurrence.topic_identifier = self.identifier
            self.__occurrences.append(occurrence)

    def remove_occurrence(self, identifier: str) -> None:
        self.__occurrences[:] = [x for x in self.__occurrences if x.identifier != identifier]

    def get_occurrence(self, identifier: str) -> Occurrence | None:
        result = None
        for occurrence in self.__occurrences:
            if occurrence.identifier == identifier:
                result = occurrence
                break
        return result

    def clear_occurrences(self) -> None:
        del self.__occurrences[:]
