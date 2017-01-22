"""
test_models.py file. Part of the StoryTechnologies project.

January 22, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.language import Language
from topicdb.core.models.topic import Topic
from topicdb.core.models.occurrence import Occurrence


class TestModels:

    def test_init_topic1(self):
        topic1 = Topic(identifier='test-topic1')

        assert topic1.identifier == 'test-topic1'
        assert topic1.instance_of == 'topic'
        assert len(topic1.base_names) == 1
        assert topic1.first_base_name.name == 'Undefined'
        assert topic1.first_base_name.language is Language.ENG
        assert len(topic1.attributes) == 0
        assert len(topic1.occurrences) == 0

    def test_init_topic2(self):
        topic2 = Topic(identifier='test-topic2',
                       instance_of='test',
                       base_name='Test Topic 2',
                       language=Language.SPA)

        assert topic2.identifier == 'test-topic2'
        assert topic2.instance_of == 'test'
        assert len(topic2.base_names) == 1
        assert topic2.first_base_name.name == 'Test Topic 2'
        assert topic2.first_base_name.language is Language.SPA
        assert len(topic2.attributes) == 0
        assert len(topic2.occurrences) == 0

    def test_init_occurrence1(self):
        occurrence1 = Occurrence()

        assert occurrence1.topic_identifier == ''
        assert occurrence1.instance_of == 'occurrence'
        assert occurrence1.scope == '*'
        assert occurrence1.resource_ref == ''
        assert occurrence1.resource_data is None
        assert occurrence1.language is Language.ENG
        assert len(occurrence1.attributes) == 0

    def test_init_occurrence2(self):
        occurrence2 = Occurrence(instance_of='test',
                                 topic_identifier='test-topic1',
                                 scope='test-scope',
                                 resource_ref='http://example.com/resource.pdf',
                                 language=Language.DEU)

        assert occurrence2.topic_identifier == 'test-topic1'
        assert occurrence2.instance_of == 'test'
        assert occurrence2.scope == 'test-scope'
        assert occurrence2.resource_ref == 'http://example.com/resource.pdf'
        assert occurrence2.resource_data is None
        assert occurrence2.language is Language.DEU
        assert len(occurrence2.attributes) == 0

    def test_init_association1(self):
        pass

    def test_init_association2(self):
        pass

    def test_init_attribute1(self):
        pass

    def test_init_attribute2(self):
        pass
