"""
test_topicstore.py file. Part of the StoryTechnologies project.

February 24, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)

To run tests in the terminal: brettk@brettk-X550CC:~/Source/storytechnologies/topic_db$ python -m pytest -v
"""

from topicdb.core.models.association import Association
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.store.retrievaloption import RetrievalOption

from topicdb.core.store.topicstore import TopicStore

TOPIC_MAP_IDENTIFIER = 1


def test_topic():
    topic1 = Topic(identifier='test-topic1',
                   base_name='Test Topic 1',
                   language=Language.SPA)

    # Instantiate and open topic store.
    store = TopicStore("localhost", "storytech", "5t0ryt3ch!")
    store.open()

    # Persist topic to store.
    if not store.topic_exists(TOPIC_MAP_IDENTIFIER, 'test-topic1'):
        store.set_topic(TOPIC_MAP_IDENTIFIER, topic1)

    # Retrieve topic from store.
    topic2 = store.get_topic(TOPIC_MAP_IDENTIFIER, 'test-topic1',
                             resolve_attributes=RetrievalOption.RESOLVE_ATTRIBUTES)

    store.close()

    assert topic2.identifier == 'test-topic1'
    assert topic2.instance_of == 'topic'
    assert len(topic2.base_names) == 1
    assert topic2.first_base_name.name == 'Test Topic 1'
    assert topic2.first_base_name.language is Language.SPA
    assert len(topic2.attributes) == 1
    assert len(topic2.occurrences) == 0


def test_occurrence():
    occurrence1 = Occurrence(identifier='test-occurrence1',
                             topic_identifier='test-topic1',
                             resource_ref='http://example.com/resource.pdf',
                             language=Language.DEU)

    # Instantiate and open topic store.
    store = TopicStore("localhost", "storytech", "5t0ryt3ch!")
    store.open()

    # Persist occurrence to store.
    if not store.occurrence_exists(TOPIC_MAP_IDENTIFIER, 'test-occurrence1'):
        store.set_occurrence(TOPIC_MAP_IDENTIFIER, occurrence1)

    # Retrieve occurrence from store.
    occurrence2 = store.get_occurrence(TOPIC_MAP_IDENTIFIER, 'test-occurrence1',
                                       resolve_attributes=RetrievalOption.RESOLVE_ATTRIBUTES)

    store.close()

    assert occurrence2.identifier == 'test-occurrence1'
    assert occurrence2.topic_identifier == 'test-topic1'
    assert occurrence2.instance_of == 'occurrence'
    assert occurrence2.scope == '*'  # Universal scope.
    assert occurrence2.resource_ref == 'http://example.com/resource.pdf'
    assert occurrence2.resource_data is None
    assert occurrence2.language is Language.DEU
    assert len(occurrence2.attributes) == 1


def test_topic_occurrences():
    # Instantiate and open topic store.
    store = TopicStore("localhost", "storytech", "5t0ryt3ch!")
    store.open()

    # Retrieve topic from store.
    topic2 = store.get_topic(TOPIC_MAP_IDENTIFIER, 'test-topic1',
                             resolve_attributes=RetrievalOption.RESOLVE_ATTRIBUTES,
                             resolve_occurrences=RetrievalOption.RESOLVE_OCCURRENCES)

    store.close()

    assert topic2.identifier == 'test-topic1'
    assert topic2.instance_of == 'topic'
    assert len(topic2.base_names) == 1
    assert topic2.first_base_name.name == 'Test Topic 1'
    assert topic2.first_base_name.language is Language.SPA
    assert len(topic2.attributes) == 1
    assert len(topic2.occurrences) == 2

    assert topic2.occurrences[0].identifier == 'test-occurrence1'
    assert topic2.occurrences[0].topic_identifier == 'test-topic1'
    assert topic2.occurrences[0].instance_of == 'occurrence'
    assert topic2.occurrences[0].scope == '*'  # Universal scope.
    assert topic2.occurrences[0].resource_ref == 'http://example.com/resource.pdf'
    assert topic2.occurrences[0].resource_data is None
    assert topic2.occurrences[0].language is Language.DEU
    assert len(topic2.occurrences[0].attributes) == 0


def test_occurrence_resource_data():
    resource_data = '<p>This is some text with a <a href="https://www.google.com">test</a> link.</p>'
    occurrence1 = Occurrence(identifier='test-occurrence2',
                             topic_identifier='test-topic1',
                             resource_data=resource_data)

    # Instantiate and open topic store.
    store = TopicStore("localhost", "storytech", "5t0ryt3ch!")
    store.open()

    # Persist occurrence to store.
    if not store.occurrence_exists(TOPIC_MAP_IDENTIFIER, 'test-occurrence2'):
        store.set_occurrence(TOPIC_MAP_IDENTIFIER, occurrence1)

    # Retrieve occurrence from store.
    occurrence2 = store.get_occurrence(TOPIC_MAP_IDENTIFIER, 'test-occurrence2',
                                       resolve_attributes=RetrievalOption.RESOLVE_ATTRIBUTES,
                                       inline_resource_data=RetrievalOption.INLINE_RESOURCE_DATA)

    store.close()

    # Converting the resource data from bytes to string.
    assert occurrence2.resource_data.decode("utf-8") == '<p>This is some text with a <a href="https://www.google.com">test</a> link.</p>'


def test_association():
    association1 = Association(identifier='test-association1',
                               src_topic_ref='test-topic1',
                               dest_topic_ref='test-topic2')

    # Instantiate and open topic store.
    store = TopicStore("localhost", "storytech", "5t0ryt3ch!")
    store.open()

    # Persist association to store.
    if not store.topic_exists(TOPIC_MAP_IDENTIFIER, 'test-association1'):
        store.set_association(TOPIC_MAP_IDENTIFIER, association1)

    # Retrieve occurrence from store.
    association2 = store.get_association(TOPIC_MAP_IDENTIFIER, 'test-association1',
                                         resolve_attributes=RetrievalOption.RESOLVE_ATTRIBUTES)

    store.close()

    assert association2.identifier == 'test-association1'
    assert association2.instance_of == 'association'
    assert association2.scope == '*'  # Universal scope.
    assert len(association2.base_names) == 1
    assert association2.first_base_name.name == 'Undefined'
    assert association2.first_base_name.language is Language.ENG
    assert len(association2.attributes) == 1
    assert len(association2.occurrences) == 0
    assert len(association2.members) == 2
    assert association2.members[0].role_spec == 'related'
    assert association2.members[1].role_spec == 'related'


def test_attribute():
    attribute1 = Attribute('name', 'true', 'test-entity1',
                           identifier='test-attribute1',
                           data_type=DataType.BOOLEAN,
                           language=Language.FRA)

    # Instantiate and open topic store.
    store = TopicStore("localhost", "storytech", "5t0ryt3ch!")
    store.open()

    # Persist attribute to store.
    if not store.attribute_exists(TOPIC_MAP_IDENTIFIER, 'test-entity1', 'name'):
        store.set_attribute(TOPIC_MAP_IDENTIFIER, attribute1)

    # Retrieve attribute from store.
    attribute2 = store.get_attribute(TOPIC_MAP_IDENTIFIER, 'test-attribute1')

    store.close()

    assert attribute2.identifier == 'test-attribute1'
    assert attribute2.name == 'name'
    assert attribute2.value == 'true'
    assert attribute2.entity_identifier == 'test-entity1'
    assert attribute2.scope == '*'  # Universal scope.
    assert attribute2.data_type is DataType.BOOLEAN
    assert attribute2.language is Language.FRA
