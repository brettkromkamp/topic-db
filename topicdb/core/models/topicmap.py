"""
TopicMap class. Part of the StoryTechnologies project.

January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TopicMap:

    def __init__(self, user_identifier, identifier, name, description='', image_path='', initialised=False,
                 shared=False, promoted=False):
        self.__user_identifier = user_identifier
        self.__identifier = identifier
        self.name = name
        self.description = description
        self.image_path = image_path
        self.initialised = initialised
        self.shared = shared
        self.promoted = promoted

    @property
    def user_identifier(self):
        return self.__user_identifier

    @property
    def identifier(self):
        return self.__identifier
