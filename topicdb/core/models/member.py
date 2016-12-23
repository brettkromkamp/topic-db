"""
Member class. Part of the StoryTechnologies Builder project.

July 03, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import uuid

from slugify import slugify

from topicdb.core.topicstoreerror import TopicStoreError


class Member:

    def __init__(self, topic_ref='', role_spec='related', identifier=''):
        if role_spec == '':
            raise TopicStoreError("Empty 'role spec' parameter")
        self.__role_spec = slugify(str(role_spec))
        self.__topic_refs = [] if topic_ref == '' else [slugify(str(topic_ref))]
        self.__identifier = (str(uuid.uuid4()) if identifier == '' else slugify(str(identifier)))

    @property
    def role_spec(self):
        return self.__role_spec

    @role_spec.setter
    def role_spec(self, value):
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        self.__role_spec = slugify(str(value))

    @property
    def identifier(self):
        return self.__identifier

    @property
    def topic_refs(self):
        return self.__topic_refs

    def add_topic_ref(self, topic_ref):
        if topic_ref == '':
            raise TopicStoreError("Empty 'topic ref' parameter")
        self.__topic_refs.append(slugify(str(topic_ref)))

    def remove_topic_ref(self, topic_ref):
        self.__topic_refs[:] = [x for x in self.__topic_refs if x != topic_ref]  # TODO: Verify.

    def clear_topic_refs(self):
        del self.__topic_refs[:]
