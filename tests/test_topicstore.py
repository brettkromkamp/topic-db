"""
test_topicstore.py file. Part of the StoryTechnologies project.

February 24, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import pytest

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
    store = TopicStore("localhost", "5t0ryt3ch!")
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
    store = TopicStore("localhost", "5t0ryt3ch!")
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


def test_association():
    pass


def test_attribute():
    pass
