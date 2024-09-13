import unittest

from topicdb.models.attribute import UNIVERSAL_SCOPE, Attribute
from topicdb.models.datatype import DataType
from topicdb.models.language import Language
from topicdb.topicdberror import TopicDbError


class TestAttribute(unittest.TestCase):

    def setUp(self):
        self.attribute = Attribute(
            name="test_name",
            value="test_value",
            entity_identifier="test_entity",
            identifier="test_identifier",
            data_type=DataType.STRING,
            scope=UNIVERSAL_SCOPE,
            language=Language.ENG,
        )

    def test_initialization(self):
        self.assertEqual(self.attribute.name, "test_name")
        self.assertEqual(self.attribute.value, "test_value")
        self.assertEqual(self.attribute.entity_identifier, "test-entity")
        self.assertEqual(self.attribute.identifier, "test-identifier")
        self.assertEqual(self.attribute.data_type, DataType.STRING)
        self.assertEqual(self.attribute.scope, UNIVERSAL_SCOPE)
        self.assertEqual(self.attribute.language, Language.ENG)

    def test_entity_identifier_setter(self):
        self.attribute.entity_identifier = "new-entity"
        self.assertEqual(self.attribute.entity_identifier, "new-entity")

        with self.assertRaises(TopicDbError):
            self.attribute.entity_identifier = ""

    def test_scope_setter(self):
        self.attribute.scope = "new-scope"
        self.assertEqual(self.attribute.scope, "new-scope")

        with self.assertRaises(TopicDbError):
            self.attribute.scope = ""


if __name__ == "__main__":
    unittest.main()
