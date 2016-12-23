"""
Entity class. Part of the StoryTechnologies Builder project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import uuid

from slugify import slugify

from topicdb.core.topicstoreerror import TopicStoreError


class Entity:

    def __init__(self,
                 identifier='',
                 instance_of='entity'):
        if instance_of == '':
            raise TopicStoreError("Empty 'instance of' parameter")

        if identifier == '':
            self.__identifier = str(uuid.uuid4())
        elif identifier == '*':  # Universal Scope.
            self.__identifier = '*'
        else:
            self.__identifier = slugify(str(identifier))

        self.__instance_of = slugify(str(instance_of))
        self.__attributes = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def instance_of(self):
        return self.__instance_of

    @instance_of.setter
    def instance_of(self, value):
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        self.__instance_of = slugify(str(value))

    @property
    def attributes(self):
        return self.__attributes

    def add_attribute(self, attribute):
        self.__attributes.append(attribute)

    def add_attributes(self, attributes):
        for attribute in attributes:
            self.__attributes.append(attribute)

    def remove_attribute(self, identifier):
        self.__attributes[:] = [x for x in self.__attributes if x.identifier != identifier]

    def get_attribute(self, identifier):
        result = None
        for attribute in self.__attributes:
            if attribute.identifier == identifier:
                result = attribute
                break
        return result

    def get_attribute_by_name(self, name):
        result = None
        for attribute in self.__attributes:
            if attribute.name == name:
                result = attribute
                break
        return result

    def clear_attributes(self):
        del self.__attributes[:]
