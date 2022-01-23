"""
test_store.py file. Part of the Contextualise (https://contextualise.dev) project.

February 24, 2017
Brett Alistair Kromkamp (brettkromkamp@gmail.com)

To run tests in the terminal: $ ~/Source/storytechnologies/topic_db$ python -m pytest -v
"""

import configparser
import os

from topicdb.core.models.association import Association
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.store.retrievalmode import RetrievalMode
from topicdb.core.store.topicstore import TopicStore


def test_topic():
    topic1 = Topic(identifier="test-topic1", name="Test Topic 1", language=Language.SPA)

    # Instantiate and open topic store.
    with TopicStore() as store:

        # Persist topic to store.
        if not store.topic_exists("test-topic1"):
            store.set_topic(topic1)

        # Retrieve topic from store.
        topic2 = store.get_topic(
            "test-topic1",
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
        )

    assert topic2.identifier == "test-topic1"
    assert topic2.instance_of == "topic"
    assert len(topic2.base_names) == 1
    assert topic2.first_base_name.name == "Test Topic 1"
    assert topic2.first_base_name.language is Language.SPA
    assert len(topic2.attributes) == 1
    assert len(topic2.occurrences) == 0


def test_occurrence():
    occurrence1 = Occurrence(
        identifier="test-occurrence1",
        topic_identifier="test-topic1",
        resource_ref="http://example.com/resource.pdf",
        language=Language.DEU,
    )

    # Instantiate and open topic store.
    with TopicStore() as store:

        # Persist occurrence to store.
        if not store.occurrence_exists("test-occurrence1"):
            store.set_occurrence(occurrence1)

        # Retrieve occurrence from store.
        occurrence2 = store.get_occurrence(
            "test-occurrence1",
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
        )

    assert occurrence2.identifier == "test-occurrence1"
    assert occurrence2.topic_identifier == "test-topic1"
    assert occurrence2.instance_of == "occurrence"
    assert occurrence2.scope == "*"  # Universal scope.
    assert occurrence2.resource_ref == "http://example.com/resource.pdf"
    assert occurrence2.resource_data is None
    assert occurrence2.language is Language.DEU
    assert len(occurrence2.attributes) == 1


def test_topic_occurrences():
    # Instantiate and open topic store.
    with TopicStore() as store:

        # Retrieve topic from store.
        topic2 = store.get_topic(
            "test-topic1",
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
            resolve_occurrences=RetrievalMode.RESOLVE_OCCURRENCES,
        )

    assert topic2.identifier == "test-topic1"
    assert topic2.instance_of == "topic"
    assert len(topic2.base_names) == 1
    assert topic2.first_base_name.name == "Test Topic 1"
    assert topic2.first_base_name.language is Language.SPA
    assert len(topic2.attributes) == 1
    assert len(topic2.occurrences) >= 1

    assert topic2.occurrences[0].identifier == "test-occurrence1"
    assert topic2.occurrences[0].topic_identifier == "test-topic1"
    assert topic2.occurrences[0].instance_of == "occurrence"
    assert topic2.occurrences[0].scope == "*"  # Universal scope.
    assert topic2.occurrences[0].resource_ref == "http://example.com/resource.pdf"
    assert topic2.occurrences[0].resource_data is None
    assert topic2.occurrences[0].language is Language.DEU
    assert len(topic2.occurrences[0].attributes) == 0


def test_occurrence_resource_data():
    resource_data = b'<p>This is some text with a <a href="https://www.google.com">test</a> link.</p>'
    occurrence1 = Occurrence(
        identifier="test-occurrence2",
        topic_identifier="test-topic1",
        resource_data=resource_data,
    )

    # Instantiate and open topic store.
    with TopicStore() as store:

        # Persist occurrence to store.
        if not store.occurrence_exists("test-occurrence2"):
            store.set_occurrence(occurrence1)

        # Retrieve occurrence from store.
        occurrence2 = store.get_occurrence(
            "test-occurrence2",
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
            inline_resource_data=RetrievalMode.INLINE_RESOURCE_DATA,
        )

    # Converting the resource data from bytes to string.
    assert (
        occurrence2.resource_data.decode("utf-8")
        == '<p>This is some text with a <a href="https://www.google.com">test</a> link.</p>'
    )


def test_delete_occurrence():
    pass


def test_delete_occurrences():
    pass


def test_association():
    association1 = Association(
        identifier="test-association1",
        src_topic_ref="test-topic1",
        dest_topic_ref="test-topic2",
    )

    # Instantiate and open topic store.
    with TopicStore() as store:

        # Associations are topics, as well (in TopicDB). For that reason, to check for the existence of an
        # association we can use the *topic_exists* method.
        if not store.topic_exists("test-association1"):
            store.set_association(association1)  # Persist association to store.

        # Retrieve occurrence from store.
        association2 = store.get_association(
            "test-association1",
            resolve_attributes=RetrievalMode.RESOLVE_ATTRIBUTES,
        )

    assert association2.identifier == "test-association1"
    assert association2.instance_of == "association"
    assert association2.scope == "*"  # Universal scope.
    assert len(association2.base_names) == 1
    assert association2.first_base_name.name == "Undefined"
    assert association2.first_base_name.language is Language.ENG
    assert len(association2.attributes) == 1
    assert len(association2.occurrences) == 0
    assert len(association2.members) == 2
    assert association2.members[0].role_spec == "related"
    assert association2.members[1].role_spec == "related"


def test_delete_association():
    pass


def test_attribute():
    attribute1 = Attribute(
        "name",
        "true",
        "test-entity1",
        identifier="test-attribute1",
        data_type=DataType.BOOLEAN,
        language=Language.FRA,
    )

    # Instantiate and open topic store.
    with TopicStore() as store:

        # Persist attribute to store.
        if not store.attribute_exists("test-entity1", "name"):
            store.set_attribute(attribute1)

        # Retrieve attribute from store.
        attribute2 = store.get_attribute("test-attribute1")

    assert attribute2.identifier == "test-attribute1"
    assert attribute2.name == "name"
    assert attribute2.value == "true"
    assert attribute2.entity_identifier == "test-entity1"
    assert attribute2.scope == "*"  # Universal scope.
    assert attribute2.data_type is DataType.BOOLEAN
    assert attribute2.language is Language.FRA


def test_delete_attribute():
    pass
