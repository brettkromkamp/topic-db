"""
InitMap class. Part of the StoryTechnologies project.

July 16, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicmapengine.core.models.topic import Topic
from topicmapengine.core.commands.topic.settopic import SetTopic
from topicmapengine.core.commands.map.topicfield import TopicField


class InitMap:

    def __init__(self, database_path, map_identifier):
        self.database_path = database_path
        self.map_identifier = map_identifier

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
            ('north-west', 'Northwest')
        }

    def execute(self):
        set_topic_command = SetTopic(self.database_path, self.map_identifier)
        for item in self.items:
            topic = Topic(identifier=item[TopicField.identifier.value], base_name=item[TopicField.base_name.value])
            set_topic_command.topic = topic
            set_topic_command.execute()
