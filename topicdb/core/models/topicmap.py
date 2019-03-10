"""
TopicMap class. Part of the StoryTechnologies project.

January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TopicMap:

    def __init__(self, user_identifier, identifier, title, description='', public=False):
        self.__user_identifier = user_identifier
        self.__identifier = identifier
        self.title = title
        self.description = description
        self.public = public

    @property
    def user_identifier(self):
        return self.__user_identifier

    @property
    def identifier(self):
        return self.__identifier
