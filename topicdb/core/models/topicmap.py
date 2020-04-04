"""
TopicMap class. Part of the StoryTechnologies project.

January 07, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.store.collaborationmode import CollaborationMode


class TopicMap:
    def __init__(
        self,
        user_identifier: int,
        identifier: int,
        name: str,
        description: str = "",
        image_path: str = "",
        initialised: bool = False,
        published: bool = False,
        promoted: bool = False,
        owner: bool = False,
        collaboration_mode: CollaborationMode = CollaborationMode.CAN_VIEW,
    ) -> None:
        self.__user_identifier = user_identifier
        self.__identifier = identifier
        self.name = name
        self.description = description
        self.image_path = image_path
        self.initialised = initialised
        self.published = published
        self.promoted = promoted
        self.owner = owner
        self.collaboration_mode = collaboration_mode

    @property
    def user_identifier(self) -> int:
        return self.__user_identifier

    @property
    def identifier(self) -> int:
        return self.__identifier
