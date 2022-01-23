"""
Map class. Part of the Contextualise (https://contextualise.dev) project.
January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.collaborationmode import CollaborationMode


class Map:
    def __init__(
        self,
        identifier: int,
        name: str,
        user_identifier: int = None,
        description: str = "",
        image_path: str = "",
        initialised: bool = False,
        published: bool = False,
        promoted: bool = False,
        owner: bool = None,
        collaboration_mode: CollaborationMode = None,
    ) -> None:
        self.__identifier = identifier
        self.name = name
        self.user_identifier = user_identifier
        self.description = description
        self.image_path = image_path
        self.initialised = initialised
        self.published = published
        self.promoted = promoted
        self.owner = owner
        self.collaboration_mode = collaboration_mode

    @property
    def identifier(self) -> int:
        return self.__identifier
