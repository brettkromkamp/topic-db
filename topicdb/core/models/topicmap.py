"""
TopicMap class. Part of the StoryTechnologies project.

January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TopicMap:
    def __init__(
        self,
        user_identifier: int,
        identifier: int,
        name: str,
        description: str = "",
        image_path: str = "",
        initialised: bool = False,
        shared: bool = False,
        promoted: bool = False,
    ) -> None:
        self.__user_identifier = user_identifier
        self.__identifier = identifier
        self.name = name
        self.description = description
        self.image_path = image_path
        self.initialised = initialised
        self.shared = shared
        self.promoted = promoted

    @property
    def user_identifier(self) -> int:
        return self.__user_identifier

    @property
    def identifier(self) -> int:
        return self.__identifier
