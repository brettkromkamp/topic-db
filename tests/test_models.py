"""
test_models.py file. Part of the StoryTechnologies project.

January 22, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language
from topicdb.core.models.topic import Topic
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.association import Association
from topicdb.core.models.attribute import Attribute


def test_init_topic1():
    topic1 = Topic(identifier="test-topic1")

    assert topic1.identifier == "test-topic1"
    assert topic1.instance_of == "topic"
    assert len(topic1.base_names) == 1
    assert topic1.first_base_name.name == "Undefined"
    assert topic1.first_base_name.language is Language.ENG
    assert len(topic1.attributes) == 0
    assert len(topic1.occurrences) == 0


def test_init_topic2():
    topic2 = Topic(
        identifier="test-topic2",
        instance_of="test",
        name="Test Topic 2",
        language=Language.SPA,
    )

    assert topic2.identifier == "test-topic2"
    assert topic2.instance_of == "test"
    assert len(topic2.base_names) == 1
    assert topic2.first_base_name.name == "Test Topic 2"
    assert topic2.first_base_name.language is Language.SPA
    assert len(topic2.attributes) == 0
    assert len(topic2.occurrences) == 0


def test_init_occurrence1():
    occurrence1 = Occurrence()

    assert occurrence1.topic_identifier == ""
    assert occurrence1.instance_of == "occurrence"
    assert occurrence1.scope == "*"  # Universal Scope.
    assert occurrence1.resource_ref == ""
    assert occurrence1.resource_data is None
    assert occurrence1.language is Language.ENG
    assert len(occurrence1.attributes) == 0


def test_init_occurrence2():
    occurrence2 = Occurrence(
        instance_of="test",
        topic_identifier="test-topic1",
        scope="test-scope",
        resource_ref="http://example.com/resource.pdf",
        language=Language.DEU,
    )

    assert occurrence2.topic_identifier == "test-topic1"
    assert occurrence2.instance_of == "test"
    assert occurrence2.scope == "test-scope"
    assert occurrence2.resource_ref == "http://example.com/resource.pdf"
    assert occurrence2.resource_data is None
    assert occurrence2.language is Language.DEU
    assert len(occurrence2.attributes) == 0


def test_init_association1():
    association1 = Association()

    assert association1.instance_of == "association"
    assert association1.scope == "*"  # Universal Scope.
    assert len(association1.base_names) == 1
    assert association1.first_base_name.name == "Undefined"
    assert association1.first_base_name.language is Language.ENG
    assert len(association1.attributes) == 0
    assert len(association1.occurrences) == 0
    assert len(association1.members) == 0


def test_init_association2():
    association2 = Association(
        instance_of="test",
        scope="test-scope",
        src_topic_ref="test-topic1",
        dest_topic_ref="test-topic2",
    )

    assert association2.instance_of == "test"
    assert association2.scope == "test-scope"
    assert len(association2.base_names) == 1
    assert association2.first_base_name.name == "Undefined"
    assert association2.first_base_name.language is Language.ENG
    assert len(association2.attributes) == 0
    assert len(association2.occurrences) == 0
    assert len(association2.members) == 2
    assert association2.members[0].role_spec == "related"
    assert association2.members[1].role_spec == "related"


def test_init_attribute1():
    attribute1 = Attribute("name", "value", "test-entity1")

    assert attribute1.name == "name"
    assert attribute1.value == "value"
    assert attribute1.entity_identifier == "test-entity1"
    assert attribute1.scope == "*"  # Universal scope.
    assert attribute1.data_type is DataType.STRING
    assert attribute1.language is Language.ENG


def test_init_attribute2():
    attribute2 = Attribute(
        "name",
        "true",
        "test-entity1",
        scope="test-scope",
        data_type=DataType.BOOLEAN,
        language=Language.FRA,
    )

    assert attribute2.name == "name"
    assert attribute2.value == "true"
    assert attribute2.entity_identifier == "test-entity1"
    assert attribute2.scope == "test-scope"
    assert attribute2.data_type is DataType.BOOLEAN
    assert attribute2.language is Language.FRA
