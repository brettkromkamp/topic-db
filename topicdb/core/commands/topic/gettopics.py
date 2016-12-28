"""
GetTopics class. Part of the StoryTechnologies project.

July 31, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.retrievaloption import RetrievalOption
from topicdb.core.commands.topic.gettopic import GetTopic
from topicdb.core.models.language import Language
from topicdb.core.topicstoreerror import TopicStoreError


class GetTopics:

    def __init__(self, database_path, map_identifier,
                 instance_of='',
                 resolve_attributes=RetrievalOption.dont_resolve_attributes,
                 language=Language.eng,
                 offset=0,
                 limit=100):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.instance_of = instance_of
        self.resolve_attributes = resolve_attributes
        self.language = language
        self.offset = offset
        self.limit = limit

    def execute(self):
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            if self.instance_of == '':
                sql = "SELECT identifier FROM topic WHERE topicmap_identifier = ? AND scope IS NULL ORDER BY identifier LIMIT ? OFFSET ?"
                bind_variables = (self.map_identifier, self.limit, self.offset)
            else:
                sql = "SELECT identifier FROM topic WHERE topicmap_identifier = ? AND instance_of = ? AND scope IS NULL ORDER BY identifier LIMIT ? OFFSET ?"
                bind_variables = (self.map_identifier, self.instance_of, self.limit, self.offset)

            cursor.execute(sql, bind_variables)
            records = cursor.fetchall()
            for record in records:
                result.append(GetTopic(self.database_path, self.map_identifier, record['identifier'], self.resolve_attributes, self.language).execute())
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
