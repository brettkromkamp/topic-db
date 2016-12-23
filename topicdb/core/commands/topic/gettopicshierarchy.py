"""
GetTopicsHierarchy class. Part of the StoryTechnologies project.

November 20, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.commands.topic.gettopic import GetTopic
from topicdb.core.topicstoreerror import TopicStoreError
from topicdb.core.commands.association.getassociations import GetAssociations
from topicdb.core.commands.association.getassociationgroups import GetAssociationGroups
from topicdb.core.models.tree.tree import Tree
from topicdb.core.models.associationfield import AssociationField


class GetTopicsHierarchy:

    def __init__(self, database_path, map_identifier,
                 identifier='',
                 cumulative_distance=0,
                 accumulative_tree=None,
                 accumulative_nodes=None):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier
        self.cumulative_distance = cumulative_distance
        self.accumulative_tree = accumulative_tree
        self.accumulative_nodes = accumulative_nodes

        self.maximum_distance = 10

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        if self.accumulative_tree is None:
            tree = Tree()
            root_topic = GetTopic(self.database_path, self.map_identifier, self.identifier).execute()
            tree.add_node(self.identifier, parent=None, topic=root_topic)
        else:
            tree = self.accumulative_tree

        if self.accumulative_nodes is None:
            nodes = []
        else:
            nodes = self.accumulative_nodes

        if self.cumulative_distance <= self.maximum_distance:  # Exit case.
            associations = GetAssociations(self.database_path, self.map_identifier, self.identifier).execute()
            for association in associations:
                resolved_topic_refs = GetAssociationGroups._resolve_topic_refs(association)
                for resolved_topic_ref in resolved_topic_refs:
                    topic_ref = resolved_topic_ref[AssociationField.topic_ref.value]
                    if topic_ref != self.identifier and topic_ref not in nodes:
                        topic = GetTopic(self.database_path, self.map_identifier, topic_ref).execute()
                        tree.add_node(topic_ref, parent=self.identifier, topic=topic)
                    if topic_ref not in nodes:
                        nodes.append(topic_ref)
            children = tree[self.identifier].children
            for child in children:
                self.cumulative_distance += 1
                self.identifier = child
                self.accumulative_tree = tree
                self.accumulative_nodes = nodes
                self.execute()  # Recursive call.
        return tree
