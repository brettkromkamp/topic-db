"""
TopicMap class. Part of the Contextualise (https://contextualise.dev) project.

January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TopicMap:
    def __init__(
        self,
        identifier: int,
        name: str,
        user_identifier: int = None,
        description: str = "",
        image_path: str = "",
        initialised: bool = False,
    ) -> None:
        self.__identifier = identifier
        self.name = name
        self.user_identifier = user_identifier
        self.description = description
        self.image_path = image_path
        self.initialised = initialised

    @property
    def identifier(self) -> int:
        return self.__identifier
