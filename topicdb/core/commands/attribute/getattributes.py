"""
GetAttributes class. Part of the StoryTechnologies project.

July 04, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.models.language import Language
from topicdb.core.models.datatype import DataType
from topicdb.core.models.attribute import Attribute
from topicdb.core.topicstoreerror import TopicStoreError


class GetAttributes:

    def __init__(self, database_path, map_identifier,
                 entity_identifier='',
                 scope='*',
                 language=Language.eng):
        self.database_path = database_path
        self.map_identifier = map_identifier
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
            cursor.execute("SELECT * FROM attribute WHERE topicmap_identifier = ? AND parent_identifier_fk = ? AND scope = ? AND language = ?",
                           (self.map_identifier, self.entity_identifier, self.scope, self.language.name))
            records = cursor.fetchall()
            for record in records:
                attribute = Attribute(
                    record['name'],
                    record['value'],
                    record['parent_identifier_fk'],
                    record['identifier'],
                    DataType[record['data_type']],
                    record['scope'],
                    Language[record['language']])
                result.append(attribute)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
