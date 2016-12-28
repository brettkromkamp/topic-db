"""
SetTag class. Part of the StoryTechnologies project.

August 29, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.topicstoreerror import TopicStoreError
from topicdb.core.commands.association.setassociation import SetAssociation
from topicdb.core.commands.topic.topicexists import TopicExists
from topicdb.core.commands.topic.settopic import SetTopic
from topicdb.core.models.association import Association
from topicdb.core.models.topic import Topic


class SetTag:

    def __init__(self, database_path, map_identifier,
                 identifier='',
                 tag=''):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier
        self.tag = tag

    def execute(self):
        if self.tag == '' or self.identifier == '':
            raise TopicStoreError("Missing 'tag' or 'identifier' parameter")

        if not TopicExists(self.database_path, self.map_identifier, self.identifier).execute():
            identifier_topic = Topic(identifier=self.identifier,
                                     base_name=self.identifier.capitalize())
            SetTopic(self.database_path, self.map_identifier, identifier_topic).execute()

        if not TopicExists(self.database_path, self.map_identifier, self.tag).execute():
            tag_topic = Topic(identifier=self.tag, base_name=self.tag.capitalize())
            SetTopic(self.database_path, self.map_identifier, tag_topic).execute()

        tag_association1 = Association(
            instance_of='categorization',
            src_topic_ref=self.identifier,
            dest_topic_ref=self.tag,
            src_role_spec='member',
            dest_role_spec='category')
        tag_association2 = Association(
            instance_of='categorization',
            src_topic_ref='tags',
            dest_topic_ref=self.tag,
            src_role_spec='broader',
            dest_role_spec='narrower')
        SetAssociation(self.database_path, self.map_identifier, tag_association1).execute()
        SetAssociation(self.database_path, self.map_identifier, tag_association2).execute()
