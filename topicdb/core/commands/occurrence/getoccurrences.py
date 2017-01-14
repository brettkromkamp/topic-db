"""
GetOccurrences class. Part of the StoryTechnologies project.

January 11, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.attribute.getattributes import GetAttributes
from topicdb.core.commands.occurrence.getoccurrencedata import GetOccurrenceData
from topicdb.core.commands.retrievaloption import RetrievalOption
from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence


class GetOccurrences:

    def __init__(self, database_path, topic_map_identifier,
                 instance_of=None,
                 scope=None,
                 language=None,
                 offset=0,
                 limit=100,
                 inline_resource_data=RetrievalOption.DONT_INLINE_RESOURCE_DATA,
                 resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.instance_of = instance_of
        self.scope = scope
        self.language = language
        self.offset = offset
        self.limit = limit
        self.inline_resource_data = inline_resource_data
        self.resolve_attributes = resolve_attributes

    def execute(self):
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM occurrence WHERE topicmap_identifier = ? {0}"
            if self.instance_of is None:
                if self.scope is None:
                    if self.language is None:
                        query_filter = ""
                        bind_variables = (self.topic_map_identifier, )
                    else:
                        query_filter = " AND language = ?"
                        bind_variables = (self.topic_map_identifier, self.language.name.lower())
                else:
                    if self.language is None:
                        query_filter = " AND scope = ?"
                        bind_variables = (self.topic_map_identifier, self.scope)
                    else:
                        query_filter = " AND scope = ? AND language = ?"
                        bind_variables = (self.topic_map_identifier, self.scope, self.language.name.lower())
            else:
                if self.scope is None:
                    if self.language is None:
                        query_filter = " AND instance_of = ?"
                        bind_variables = (self.topic_map_identifier, self.instance_of)
                    else:
                        query_filter = " AND instance_of = ? AND language = ?"
                        bind_variables = (self.topic_map_identifier, self.instance_of, self.language.name.lower())
                else:
                    if self.language is None:
                        query_filter = " AND instance_of = ? AND scope = ?"
                        bind_variables = (self.topic_map_identifier, self.instance_of, self.scope)
                    else:
                        query_filter = " AND instance_of = ? AND scope = ? AND language = ?"
                        bind_variables = (self.topic_map_identifier, self.instance_of, self.scope, self.language.name.lower())
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                resource_data = None
                if self.inline_resource_data:
                    resource_data = GetOccurrenceData(self.database_path, self.topic_map_identifier, record['identifier']).execute()
                occurrence = Occurrence(
                    record['identifier'],
                    record['instance_of'],
                    record['topic_identifier_fk'],
                    record['scope'],
                    record['resource_ref'],
                    resource_data,
                    Language[record['language'].upper()])
                if self.resolve_attributes is RetrievalOption.RESOLVE_ATTRIBUTES:
                    occurrence.add_attributes(GetAttributes(self.database_path, self.topic_map_identifier, occurrence.identifier).execute())
                result.append(occurrence)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
