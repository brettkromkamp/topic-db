"""
GetAssociationGroups class. Part of the StoryTechnologies project.

July 13, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.doublekeydict import DoubleKeyDict
from topicdb.core.models.associationfield import AssociationField
from topicdb.core.topicstoreerror import TopicStoreError
from topicdb.core.commands.association.getassociations import GetAssociations


class GetAssociationGroups:

    def __init__(self,
                 database_path='',
                 map_identifier=None,
                 identifier='',
                 associations=None):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier
        self.associations = associations

    def execute(self):
        # TODO: Review logic for lines 26-34.
        if self.identifier == '' and self.associations is None:
            raise TopicStoreError(
                "At least one of the 'identifier' or 'associations' parameters is required")

        if self.associations is None and (self.database_path == '' or self.map_identifier is None):
            raise TopicStoreError("Missing 'database path' or 'map identifier' parameters")

        result = DoubleKeyDict()
        if not self.associations:
            self.associations = GetAssociations(self.database_path, self.map_identifier,
                                                self.identifier).execute()

        for association in self.associations:
            resolved_topic_refs = self._resolve_topic_refs(association)
            for resolved_topic_ref in resolved_topic_refs:
                instance_of = resolved_topic_ref[AssociationField.instance_of.value]
                role_spec = resolved_topic_ref[AssociationField.role_spec.value]
                topic_ref = resolved_topic_ref[AssociationField.topic_ref.value]
                if topic_ref != self.identifier:
                    if [instance_of, role_spec] in result:
                        topic_refs = result[instance_of, role_spec]
                        if topic_ref not in topic_refs:
                            topic_refs.append(topic_ref)
                        result[instance_of, role_spec] = topic_refs
                    else:
                        result[instance_of, role_spec] = [topic_ref]
        return result

    @staticmethod
    def _resolve_topic_refs(association):
        topic_refs = []
        for member in association.members:
            for topic_ref in member.topic_refs:
                topic_refs.append([association.instance_of, member.role_spec, topic_ref])
        return topic_refs
