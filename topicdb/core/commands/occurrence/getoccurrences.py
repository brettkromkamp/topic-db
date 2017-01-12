"""
GetOccurrences class. Part of the StoryTechnologies project.

January 11, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.commands.retrievaloption import RetrievalOption


class GetOccurrences:

    def __init__(self, database_path, topic_map_identifier,
                 instance_of=None,
                 scope=None,
                 language=None,
                 offset=0,
                 limit=100,
                 inline_resource_data=RetrievalOption.DONT_INLINE_RESOURCE_DATA,
                 resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES):
        pass
