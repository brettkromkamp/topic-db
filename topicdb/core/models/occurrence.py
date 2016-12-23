"""
Occurrence class. Part of the StoryTechnologies Builder project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from slugify import slugify

from topicdb.core.models.entity import Entity
from topicdb.core.models.language import Language
from topicdb.core.topicstoreerror import TopicStoreError


class Occurrence(Entity):

    def __init__(self,
                 identifier='',
                 instance_of='occurrence',
                 topic_identifier='',
                 scope='*',  # Universal scope
                 resource_ref='',
                 resource_data=None,
                 language=Language.eng):
        super().__init__(identifier, instance_of)

        if topic_identifier == '*':  # Universal Scope.
            self.__topic_identifier = '*'
        else:
            self.__topic_identifier = slugify(str(topic_identifier))

        self.__scope = scope if scope == '*' else slugify(str(scope))

        self.resource_ref = resource_ref
        self.resource_data = resource_data
        self.language = language

    @property
    def scope(self):
        return self.__scope

    @scope.setter
    def scope(self, value):
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        self.__scope = value if value == '*' else slugify(str(value))

    @property
    def topic_identifier(self):
        return self.__topic_identifier

    @topic_identifier.setter
    def topic_identifier(self, value):
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        elif value == '*':  # Universal Scope.
            self.__topic_identifier = '*'
        else:
            self.__topic_identifier = slugify(str(value))

    def has_data(self):
        return self.resource_data is not None
