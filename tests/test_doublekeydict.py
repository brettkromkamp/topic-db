import unittest

from topicdb.models.doublekeydict import DoubleKeyDict


class TestDoubleKeyDict(unittest.TestCase):

    def setUp(self):
        self.dkd = DoubleKeyDict()

    def test_set_and_get_item(self):
        self.dkd["key1", "key2"] = "value"
        self.assertEqual(self.dkd["key1", "key2"], "value")

    def test_contains(self):
        self.dkd["key1", "key2"] = "value"
        self.assertTrue(("key1", "key2") in self.dkd)
        self.assertFalse(("key1", "key3") in self.dkd)

    def test_len(self):
        self.dkd["key1", "key2"] = "value"
        self.dkd["key3", "key4"] = "another value"
        self.assertEqual(len(self.dkd), 2)

    def test_property_dict(self):
        self.dkd["key1", "key2"] = "value"
        self.assertEqual(self.dkd.dict, {"key1": {"key2": "value"}})


if __name__ == "__main__":
    unittest.main()
