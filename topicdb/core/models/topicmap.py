"""
TopicMap class. Part of the Contextualise (https://contextualise.dev) project.

January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TopicMap:
    def __init__(
        self,
        name: str,
        description: str = "",
        image_path: str = "",
        initialised: bool = False,
    ) -> None:
        self.name = name
        self.description = description
        self.image_path = image_path
        self.initialised = initialised

    @property
    def identifier(self) -> int:
        return self.__identifier
