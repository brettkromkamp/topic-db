"""
GetTopicIdentifiers class. Part of the StoryTechnologies project.

August 03, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.topicstoreerror import TopicStoreError
from topicdb.core.retrievaloption import RetrievalOption


class GetTopicIdentifiers:

    def __init__(self, database_path, map_identifier,
                 query,
                 filter_entities=RetrievalOption.dont_filter_entities,
                 offset=0,
                 limit=100):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.query = query
        self.filter_entities = filter_entities
        self.offset = offset
        self.limit = limit

    def execute(self):
        result = []

        query_string = "{0}%".format(self.query)

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            if self.filter_entities == RetrievalOption.filter_entities:
                sql = "SELECT identifier FROM topic WHERE topicmap_identifier = ? AND identifier LIKE ? AND scope IS NULL AND instance_of IN ('scene', 'prop', 'character') ORDER BY identifier LIMIT ? OFFSET ?"
            else:
                sql = "SELECT identifier FROM topic WHERE topicmap_identifier = ? AND identifier LIKE ? AND scope IS NULL ORDER BY identifier LIMIT ? OFFSET ?"
            cursor.execute(sql, (self.map_identifier, query_string, self.limit, self.offset))
            records = cursor.fetchall()
            for record in records:
                result.append(record['identifier'])
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
