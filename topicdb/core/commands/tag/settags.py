"""
SetTags class. Part of the StoryTechnologies project.

August 29, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.commands.tag.settag import SetTag
from topicdb.core.commands.topicstoreerror import TopicStoreError


class SetTags:

    def __init__(self, database_path, topic_map_identifier,
                 identifier='',
                 tags=None):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.identifier = identifier
        self.tags = tags

    def execute(self):
        if self.tags is None or self.identifier == '':
            raise TopicStoreError("Missing 'tags' or 'identifier' parameter")

        for tag in self.tags:
            SetTag(self.database_path, self.topic_map_identifier, self.identifier, tag).execute()
