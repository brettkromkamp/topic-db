"""
GetAttributes class. Part of the StoryTechnologies project.

July 04, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language


class GetAttributes:

    def __init__(self, database_path, topic_map_identifier,
                 entity_identifier='',
                 scope=None,
                 language=None):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.entity_identifier = entity_identifier
        self.scope = scope
        self.language = language

    def execute(self):
        if self.entity_identifier == '':
            raise TopicStoreError("Missing 'entity identifier' parameter")
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            if self.scope is None:
                if self.language is None:
                    sql = "SELECT * FROM attribute WHERE topicmap_identifier = ? AND parent_identifier_fk = ?"
                    bind_variables = (self.topic_map_identifier, self.entity_identifier)
                else:
                    sql = "SELECT * FROM attribute WHERE topicmap_identifier = ? AND parent_identifier_fk = ? AND language = ?"
                    bind_variables = (self.topic_map_identifier, self.entity_identifier, self.language.name.lower())
            else:
                if self.language is None:
                    sql = "SELECT * FROM attribute WHERE topicmap_identifier = ? AND parent_identifier_fk = ? AND scope = ?"
                    bind_variables = (self.topic_map_identifier, self.entity_identifier, self.scope)
                else:
                    sql = "SELECT * FROM attribute WHERE topicmap_identifier = ? AND parent_identifier_fk = ? AND scope = ? AND language = ?"
                    bind_variables = (self.topic_map_identifier, self.entity_identifier, self.scope, self.language.name.lower())

            cursor.execute(sql, bind_variables)
            records = cursor.fetchall()
            for record in records:
                attribute = Attribute(
                    record['name'],
                    record['value'],
                    record['parent_identifier_fk'],
                    record['identifier'],
                    DataType[record['data_type'].upper()],
                    record['scope'],
                    Language[record['language'].upper()])
                result.append(attribute)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
