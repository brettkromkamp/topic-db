"""
SetAttributes class. Part of the StoryTechnologies project.

July 13, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.commands.attribute.setattribute import SetAttribute
from topicdb.core.commands.topicstoreerror import TopicStoreError


class SetAttributes:

    def __init__(self, database_path, topic_map_identifier, attributes=None):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.attributes = attributes

    def execute(self):
        if self.attributes is None:
            raise TopicStoreError("Missing 'attributes' parameter")

        set_attribute_command = SetAttribute(self.database_path, self.topic_map_identifier)
        for attribute in self.attributes:
            set_attribute_command.attribute = attribute
            set_attribute_command.execute()
