"""
test_commands.py file. Part of the StoryTechnologies project.

January 22, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import os
import pytest

from topicdb.core.commands.association.getassociation import GetAssociation
from topicdb.core.commands.association.setassociation import SetAssociation
from topicdb.core.commands.attribute.getattribute import GetAttribute
from topicdb.core.commands.attribute.setattribute import SetAttribute
from topicdb.core.commands.occurrence.getoccurrence import GetOccurrence
from topicdb.core.models.association import Association
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic

from topicdb.core.commands.topicmap.settopicmap import SetTopicMap
from topicdb.core.commands.topic.gettopic import GetTopic
from topicdb.core.commands.topic.settopic import SetTopic
from topicdb.core.commands.occurrence.setoccurrence import SetOccurrence

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../data/topicmap-test.db')
TOPIC_MAP_IDENTIFIER = 1
TITLE = 'Test Topic Map'
DESCRIPTION = 'Default test topic map'


@pytest.fixture()
def topic_map():
    if os.path.isfile(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        SetTopicMap(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, TITLE, DESCRIPTION).execute()


def test_topic(topic_map):
    topic1 = Topic(identifier='test-topic2',
                   base_name='Test Topic 2',
                   language=Language.SPA)

    # Persist topic to topic store.
    SetTopic(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, topic1).execute()

    # Retrieve topic from topic store.
    topic2 = GetTopic(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, 'test-topic2').execute()

    assert topic2.identifier == 'test-topic2'
    assert topic2.instance_of == 'topic'
    assert len(topic2.base_names) == 1
    assert topic2.first_base_name.name == 'Test Topic 2'
    assert topic2.first_base_name.language is Language.SPA
    assert len(topic2.attributes) == 0
    assert len(topic2.occurrences) == 0


def test_occurrence(topic_map):
    occurrence1 = Occurrence(identifier='test-occurrence1',
                             topic_identifier='test-topic1',
                             resource_ref='http://example.com/resource.pdf',
                             language=Language.DEU)

    # Persist occurrence to topic store.
    SetOccurrence(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, occurrence1).execute()

    # Retrieve occurrence from topic store.
    occurrence2 = GetOccurrence(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, identifier='test-occurrence1').execute()

    assert occurrence2.identifier == 'test-occurrence1'
    assert occurrence2.topic_identifier == 'test-topic1'
    assert occurrence2.instance_of == 'occurrence'
    assert occurrence2.scope == '*'  # Universal scope.
    assert occurrence2.resource_ref == 'http://example.com/resource.pdf'
    assert occurrence2.resource_data is None
    assert occurrence2.language is Language.DEU
    assert len(occurrence2.attributes) == 0


def test_association(topic_map):
    association1 = Association(identifier='test-association1',
                               src_topic_ref='test-topic1',
                               dest_topic_ref='test-topic2')

    # Persist association to topic store.
    SetAssociation(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, association1).execute()

    # Retrieve association from topic store.
    association2 = GetAssociation(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, identifier='test-association1').execute()

    assert association2.identifier == 'test-association1'
    assert association2.instance_of == 'association'
    assert association2.scope == '*'  # Universal scope.
    assert len(association2.base_names) == 1
    assert association2.first_base_name.name == 'Undefined'
    assert association2.first_base_name.language is Language.ENG
    assert len(association2.attributes) == 0
    assert len(association2.occurrences) == 0
    assert len(association2.members) == 2
    assert association2.members[0].role_spec == 'related'
    assert association2.members[1].role_spec == 'related'


def test_attribute(topic_map):
    attribute1 = Attribute('name', 'true', 'test-entity1',
                           identifier='test-attribute1',
                           data_type=DataType.BOOLEAN,
                           language=Language.FRA)

    # Persist attribute to topic store.
    SetAttribute(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, attribute1).execute()

    # Retrieve attribute from topic store.
    attribute2 = GetAttribute(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, identifier='test-attribute1').execute()

    assert attribute2.identifier == 'test-attribute1'
    assert attribute2.name == 'name'
    assert attribute2.value == 'true'
    assert attribute2.entity_identifier == 'test-entity1'
    assert attribute2.scope == '*'  # Universal scope.
    assert attribute2.data_type is DataType.BOOLEAN
    assert attribute2.language is Language.FRA
