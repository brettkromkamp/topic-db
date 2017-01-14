"""
GetAssociation class. Part of the StoryTechnologies project.

July 10, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.attribute.getattributes import GetAttributes
from topicdb.core.commands.retrievaloption import RetrievalOption
from topicdb.core.commands.topic.gettopicoccurrences import GetTopicOccurrences
from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.association import Association
from topicdb.core.models.basename import BaseName
from topicdb.core.models.language import Language
from topicdb.core.models.member import Member


class GetAssociation:

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
            raise TopicStoreError("Missing 'identifier' parameter")
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT identifier, instance_of, scope FROM topic WHERE topicmap_identifier = ? AND identifier = ? AND scope IS NOT NULL", (self.topic_map_identifier, self.identifier))
            association_record = cursor.fetchone()
            if association_record:
                result = Association(identifier=association_record['identifier'], instance_of=association_record['instance_of'], scope=association_record['scope'])
                result.clear_base_names()
                if self.language is None:
                    sql = "SELECT name, language, identifier FROM basename WHERE topicmap_identifier = ? AND topic_identifier_fk = ?"
                    bind_variables = (self.topic_map_identifier, self.identifier)
                else:
                    sql = "SELECT name, language, identifier FROM basename WHERE topicmap_identifier = ? AND topic_identifier_fk = ? AND language = ?"
                    bind_variables = (self.topic_map_identifier, self.identifier, self.language.name.lower())
                cursor.execute(sql, bind_variables)
                base_name_records = cursor.fetchall()
                if base_name_records:
                    for base_name_record in base_name_records:
                        result.add_base_name(BaseName(base_name_record['name'], Language[base_name_record['language'].upper()], base_name_record['identifier']))
                cursor.execute("SELECT * FROM member WHERE topicmap_identifier = ? AND association_identifier_fk = ?", (self.topic_map_identifier, self.identifier))
                member_records = cursor.fetchall()
                if member_records:
                    for member_record in member_records:
                        role_spec = member_record['role_spec']
                        cursor.execute("SELECT * FROM topicref WHERE topicmap_identifier = ? AND member_identifier_fk = ?", (self.topic_map_identifier, member_record['identifier']))
                        topic_ref_records = cursor.fetchall()
                        if topic_ref_records:
                            member = Member(role_spec=role_spec, identifier=member_record['identifier'])
                            for topic_ref_record in topic_ref_records:
                                member.add_topic_ref(topic_ref_record['topic_ref'])
                            result.add_member(member)
                if self.resolve_attributes is RetrievalOption.RESOLVE_ATTRIBUTES:
                    result.add_attributes(GetAttributes(self.database_path, self.identifier).execute())
                if self.resolve_occurrences is RetrievalOption.RESOLVE_OCCURRENCES:
                    result.add_occurrences(GetTopicOccurrences(self.database_path, self.identifier).execute())
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
