"""
TopicMap class. Part of the StoryTechnologies project.

January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TopicMap:

    def __init__(self, title, topic_map_identifier, entry_topic_identifier='genesis', description=''):
        self.__identifier = None
        self.title = title
        self.topic_map_identifier = topic_map_identifier
        self.entry_topic_identifier = entry_topic_identifier
        self.description = description

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, value):
        if self.__identifier is None:
            self.__identifier = value
