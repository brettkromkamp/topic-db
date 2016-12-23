"""
Association class. Part of the StoryTechnologies Builder project.

July 03, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from slugify import slugify

from topicdb.core.models.topic import Topic
from topicdb.core.models.member import Member
from topicdb.core.models.language import Language
from topicdb.core.topicstoreerror import TopicStoreError


class Association(Topic):

    def __init__(self,
                 identifier='',
                 instance_of='association',
                 base_name='Undefined',
                 language=Language.eng,
                 scope='*',
                 src_topic_ref='',
                 dest_topic_ref='',
                 src_role_spec='related',
                 dest_role_spec='related'):
        super().__init__(identifier, instance_of, base_name, language)

        self.__scope = scope if scope == '*' else slugify(str(scope))
        self.__members = []

        if src_topic_ref != '' and src_role_spec != '' and dest_topic_ref != '' and dest_role_spec != '':
            src_member = Member(src_topic_ref, src_role_spec)
            dest_member = Member(dest_topic_ref, dest_role_spec)
            self.__members.append(src_member)
            self.__members.append(dest_member)

    @property
    def scope(self):
        return self.__scope

    @scope.setter
    def scope(self, value):
        if value == '':
            raise TopicStoreError("Empty 'scope' parameter")
        self.__scope = value if value == '*' else slugify(str(value))

    @property
    def members(self):
        return self.__members

    def create_member(self, topic_ref, role_spec='related'):
        member = Member(topic_ref, role_spec)
        self.add_member(member)

    def create_members(self, src_topic_ref, dest_topic_ref, src_role_spec='related', dest_role_spec='related'):
        members = [Member(src_topic_ref, src_role_spec), Member(dest_topic_ref, dest_role_spec)]
        self.add_members(members)

    def add_member(self, member):
        self.__members.append(member)

    def add_members(self, members):
        for member in members:
            self.__members.append(member)

    def remove_member(self, identifier):
        self.__members[:] = [x for x in self.__members if x.identifier != identifier]  # TODO: Verify.

    def clear_members(self):
        del self.__members[:]
