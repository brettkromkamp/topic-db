"""
GetTags class. Part of the StoryTechnologies project.

August 29, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.commands.association.getassociationgroups import GetAssociationGroups
from topicdb.core.commands.topic.gettopicassociations import GetTopicAssociations
from topicdb.core.topicstoreerror import TopicStoreError


class GetTags:

    def __init__(self, database_path, topic_map_identifier, identifier=''):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.identifier = identifier

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = []

        associations = GetTopicAssociations(
            self.database_path, self.topic_map_identifier, self.identifier).execute()
        if associations:
            groups = GetAssociationGroups(associations=associations).execute()
            for instance_of in groups.dict:
                for role in groups.dict[instance_of]:
                    for topic_ref in groups[instance_of, role]:
                        if topic_ref == self.identifier:
                            continue
                        if instance_of == 'categorization':
                            result.append(topic_ref)
        return result
