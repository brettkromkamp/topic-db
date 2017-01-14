"""
SetTopicMap class. Part of the StoryTechnologies project.

January 07, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import os
import sqlite3

from topicdb.core.commands.ontologymode import OntologyMode
from topicdb.core.commands.topic.settopic import SetTopic
from topicdb.core.commands.topic.topicexists import TopicExists
from topicdb.core.commands.topicmap.topicfield import TopicField
from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.topic import Topic


class SetTopicMap:

    def __init__(self, database_path, topic_map_identifier, title,
                 description='',
                 entry_topic='genesis'):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.title = title
        self.description = description
        self.entry_topic = entry_topic

    def execute(self):
        # Create database schema.
        self._create_map()

        # Bootstrap default topics (ontology).
        if not TopicExists(self.database_path, self.topic_map_identifier, 'genesis').execute():
            self._init_map()

    def _create_map(self):
        connection = sqlite3.connect(self.database_path)
        definitions_file = open(
            os.path.join(os.path.dirname(__file__), '../../../conf/topicmap-definition.sql'))
        statements = definitions_file.read()

        try:
            with connection:
                for statement in statements.split(';'):
                    connection.execute(statement)
                connection.execute(
                    "INSERT INTO topicmap (title, description, topicmap_identifier_fk, entry_identifier_fk) VALUES (?, ?, ?, ?)",
                    (self.title,
                     self.description,
                     self.topic_map_identifier,
                     self.entry_topic))
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()

    def _init_map(self):
        self.items = {
            ('entity', 'Entity'),
            ('topic', 'Topic'),
            ('association', 'Association'),
            ('occurrence', 'Occurrence'),
            ('*', 'Universal Scope'),
            ('genesis', 'Genesis'),
            ('navigation', 'Navigation'),
            ('member', 'Member'),
            ('category', 'Category'),
            ('categorization', 'Categorization'),
            ('tags', 'Tags'),
            ('broader', 'Broader'),
            ('narrower', 'Narrower'),
            ('related', 'Related'),
            ('parent', 'Parent'),
            ('child', 'Child'),
            ('previous', 'Previous'),
            ('next', 'Next'),
            ('includes', 'Includes'),
            ('included-in', 'Is Included In'),
            ('story', 'Story'),
            ('book', 'Book'),
            ('chapter', 'Chapter'),
            ('scene', 'Scene'),
            ('prop', 'Prop'),
            ('character', 'Character'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('text', 'Text'),
            ('html', 'HTML'),
            ('annotation', 'Annotation'),
            ('dialogue', 'Dialogue'),
            ('up', 'Up'),
            ('down', 'Down'),
            ('north', 'North'),
            ('north-east', 'Northeast'),
            ('east', 'East'),
            ('south-east', 'Southeast'),
            ('south', 'South'),
            ('south-west', 'Southwest'),
            ('west', 'West'),
            ('north-west', 'Northwest'),
            ('eng', 'English Language'),
            ('spa', 'Spanish Language'),
            ('deu', 'German Language'),
            ('ita', 'Italian Language'),
            ('fra', 'French Language'),
            ('nld', 'Dutch Language'),
            ('nob', 'Norwegian (Bokmål) Language')}

        set_topic_command = SetTopic(self.database_path, self.topic_map_identifier, ontology_mode=OntologyMode.LENIENT)
        for item in self.items:
            topic = Topic(identifier=item[TopicField.IDENTIFIER.value], base_name=item[TopicField.BASE_NAME.value])
            set_topic_command.topic = topic
            set_topic_command.execute()
