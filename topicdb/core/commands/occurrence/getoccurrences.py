"""
GetOccurrences class. Part of the StoryTechnologies project.

July 05, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.attribute.getattributes import GetAttributes
from topicdb.core.commands.occurrence.getoccurrencedata import GetOccurrenceData
from topicdb.core.commands.retrievaloption import RetrievalOption
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.topicstoreerror import TopicStoreError


class GetOccurrences:

    def __init__(self, database_path, map_identifier,
                 topic_identifier='',
                 inline_resource_data=RetrievalOption.dont_inline_resource_data,
                 resolve_attributes=RetrievalOption.dont_resolve_attributes,
                 instance_of='',
                 scope='*',
                 language=Language.eng):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.topic_identifier = topic_identifier
        self.inline_resource_data = inline_resource_data
        self.resolve_attributes = resolve_attributes
        self.instance_of = instance_of
        self.scope = scope
        self.language = language

    def execute(self):
        if self.topic_identifier == '':
            raise TopicStoreError("Missing 'topic identifier' parameter")
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            if self.instance_of == '':
                sql = "SELECT identifier, instance_of, scope, resource_ref, topic_identifier_fk, language FROM occurrence WHERE topicmap_identifier = ? AND topic_identifier_fk = ? AND scope = ? AND language = ?"
                bind_variables = (self.map_identifier, self.topic_identifier, self.scope, self.language.name)
            else:
                sql = "SELECT identifier, instance_of, scope, resource_ref, topic_identifier_fk, language FROM occurrence WHERE topicmap_identifier = ? AND topic_identifier_fk = ? AND instance_of = ? AND scope = ? AND language = ?"
                bind_variables = (self.map_identifier, self.topic_identifier, self.instance_of, self.scope, self.language.name)

            cursor.execute(sql, bind_variables)
            records = cursor.fetchall()
            for record in records:
                resource_data = None
                if self.inline_resource_data:
                    # TODO: Optimize.
                    resource_data = GetOccurrenceData(self.database_path, self.map_identifier, record['identifier']).execute()
                occurrence = Occurrence(
                    record['identifier'],
                    record['instance_of'],
                    record['topic_identifier_fk'],
                    record['scope'],
                    record['resource_ref'],
                    resource_data,
                    Language[record['language']])
                if self.resolve_attributes is RetrievalOption.resolve_attributes:
                    # TODO: Optimize.
                    occurrence.add_attributes(
                        GetAttributes(self.database_path, self.map_identifier, occurrence.identifier).execute())
                result.append(occurrence)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
