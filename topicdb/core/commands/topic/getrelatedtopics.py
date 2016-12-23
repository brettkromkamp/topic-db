"""
GetRelatedTopics class. Part of the StoryTechnologies project.

October 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.commands.topic.gettopic import GetTopic
from topicdb.core.topicstoreerror import TopicStoreError
from topicdb.core.commands.association.getassociations import GetAssociations
from topicdb.core.commands.association.getassociationgroups import GetAssociationGroups


class GetRelatedTopics:

    def __init__(self, database_path, map_identifier, identifier=''):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = []

        associations = GetAssociations(self.database_path, self.map_identifier, self.identifier).execute()
        if associations:
            groups = GetAssociationGroups(associations=associations).execute()
            for instance_of in groups.dict:
                for role in groups.dict[instance_of]:
                    for topic_ref in groups[instance_of, role]:
                        if topic_ref == self.identifier:
                            continue
                        result.append(GetTopic(self.database_path, topic_ref).execute())
        return result
