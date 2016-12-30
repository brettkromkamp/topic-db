"""
DeleteAssociation class. Part of the StoryTechnologies project.

December 30, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.attribute.deleteattributes import DeleteAttributes
from topicdb.core.topicstoreerror import TopicStoreError


class DeleteAssociation:

    def __init__(self, database_path, map_identifier, identifier=''):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        try:
            with connection:  # https://docs.python.org/3/library/sqlite3.html#using-the-connection-as-a-context-manager
                # Delete topic/association record.
                connection.execute(
                    "DELETE FROM topic WHERE topicmap_identifier = ? AND identifier = ? AND scope IS NOT NULL",
                    (self.map_identifier, self.identifier))
                # Delete base name record(s).
                connection.execute(
                    "DELETE FROM basename WHERE topicmap_identifier = ? AND topic_identifier_fk = ?",
                    (self.map_identifier, self.identifier))
                # Get members.
                cursor.execute(
                    "SELECT identifier FROM member WHERE topicmap_identifier = ? AND association_identifier_fk = ?",
                    (self.map_identifier, self.identifier))
                member_records = cursor.fetchall()
                # Delete members.
                connection.execute(
                    "DELETE FROM member WHERE topicmap_identifier = ? AND association_identifier_fk = ?",
                    (self.map_identifier, self.identifier))
                if member_records:
                    for member_record in member_records:
                        # Delete topic refs.
                        connection.execute(
                            "DELETE FROM topicref WHERE topicmap_identifier = ? AND member_identifier_fk = ?",
                            (self.map_identifier, member_record['identifier']))
            # Delete attributes.
            DeleteAttributes(self.database_path, self.map_identifier, self.identifier)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
