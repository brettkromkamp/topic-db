"""
Topic class. Part of the StoryTechnologies Builder project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.entity import Entity
from topicdb.core.models.basename import BaseName
from topicdb.core.models.language import Language


class Topic(Entity):

    def __init__(self, identifier='', instance_of='topic', base_name='Undefined', language=Language.ENG):
        super().__init__(identifier, instance_of)

        default_base_name = BaseName(base_name, language)

        self.__base_names = [default_base_name]
        self.__occurrences = []

        self.language = language

    @property
    def base_names(self):
        return self.__base_names

    @property
    def occurrences(self):
        return self.__occurrences

    @property
    def first_base_name(self):
        if len(self.__base_names) > 0:
            result = self.__base_names[0]
        else:
            result = BaseName("Undefined", Language.ENG)
        return result

    def get_base_name(self, identifier):
        result = None
        for base_name in self.__base_names:
            if base_name.identifier == identifier:
                result = base_name
                break
        return result

    def add_base_name(self, base_name):
        self.__base_names.append(base_name)

    def add_base_names(self, base_names):
        for base_name in base_names:
            self.__base_names.append(base_name)

    def remove_base_name(self, identifier):
        self.__base_names[:] = [x for x in self.__base_names if x.identifier != identifier]

    def clear_base_names(self):
        del self.__base_names[:]

    def add_occurrence(self, occurrence):
        occurrence.topic_identifier = self.identifier
        self.__occurrences.append(occurrence)

    def add_occurrences(self, occurrences):
        for occurrence in occurrences:
            occurrence.topic_identifier = self.identifier
            self.__occurrences.append(occurrence)

    def remove_occurrence(self, identifier):
        self.__occurrences[:] = [x for x in self.__occurrences if x.identifier != identifier]

    def get_occurrence(self, identifier):
        result = None
        for occurrence in self.__occurrences:
            if occurrence.identifier == identifier:
                result = occurrence
                break
        return result

    def clear_occurrences(self):
        del self.__occurrences[:]
