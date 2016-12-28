"""
InitMap class. Part of the StoryTechnologies project.

July 16, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""
from topicdb.core.commands.ontologymode import OntologyMode
from topicdb.core.models.topic import Topic
from topicdb.core.commands.topic.settopic import SetTopic
from topicdb.core.commands.map.topicfield import TopicField


class InitMap:

    def __init__(self, database_path, map_identifier):
        self.database_path = database_path
        self.map_identifier = map_identifier

        # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        # https://en.wikipedia.org/wiki/ISO_639-2

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
            ('nob', 'Norwegian (Bokmål) Language')
        }

    def execute(self):
        set_topic_command = SetTopic(self.database_path, self.map_identifier,
                                     ontology_mode=OntologyMode.lenient)
        for item in self.items:
            topic = Topic(identifier=item[TopicField.identifier.value],
                          base_name=item[TopicField.base_name.value])
            set_topic_command.topic = topic
            set_topic_command.execute()
