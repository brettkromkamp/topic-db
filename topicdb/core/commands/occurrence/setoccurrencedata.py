"""
SetOccurrenceData class. Part of the StoryTechnologies project.

July 04, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.topicstoreerror import TopicStoreError


class SetOccurrenceData:
    def __init__(self, database_path, map_identifier,
                 identifier='',
                 resource_data=None):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier
        self.resource_data = bytes(resource_data, 'utf-8')

    def execute(self):
        if self.identifier == '' or self.resource_data is None:
            raise TopicStoreError("Missing either or both 'identifier' and 'resource data' parameters")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:
                connection.execute("UPDATE occurrence SET resource_data = ? WHERE topicmap_identifier = ? AND identifier = ?", (self.resource_data, self.map_identifier, self.identifier))
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
