"""
GetTopicAssociations class. Part of the StoryTechnologies project.

July 10, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.association.getassociation import GetAssociation
from topicdb.core.commands.retrievaloption import RetrievalOption
from topicdb.core.commands.topicstoreerror import TopicStoreError


class GetTopicAssociations:

    def __init__(self, database_path, topic_map_identifier,
                 identifier='',
                 language=None,
                 resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES,
                 resolve_occurrences=RetrievalOption.DONT_RESOLVE_OCCURRENCES):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.identifier = identifier
        self.language = language
        self.resolve_attributes = resolve_attributes
        self.resolve_occurrences = resolve_occurrences

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'topic identifier' parameter")
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT member_identifier_fk FROM topicref WHERE topicmap_identifier = ? AND TOPIC_REF = ?", (self.topic_map_identifier, self.identifier))
            topic_ref_records = cursor.fetchall()
            if topic_ref_records:
                for topic_ref_record in topic_ref_records:
                    cursor.execute("SELECT association_identifier_fk FROM member WHERE topicmap_identifier = ? AND identifier = ?", (self.topic_map_identifier, topic_ref_record['member_identifier_fk']))
                    member_records = cursor.fetchall()
                    if member_records:
                        for member_record in member_records:
                            association = GetAssociation(self.database_path,
                                                         self.topic_map_identifier,
                                                         member_record['association_identifier_fk'],
                                                         language=self.language,
                                                         resolve_attributes=self.resolve_attributes,
                                                         resolve_occurrences=self.resolve_occurrences).execute()
                            if association:
                                result.append(association)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
