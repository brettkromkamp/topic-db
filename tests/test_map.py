import unittest

from topicdb.models.collaborationmode import CollaborationMode
from topicdb.models.map import Map


class TestMap(unittest.TestCase):
    def test_init_with_required_parameters(self):
        map_instance = Map(identifier=1, name="Test Map", collaboration_mode=CollaborationMode.VIEW)
        self.assertEqual(map_instance.identifier, 1)
        self.assertEqual(map_instance.name, "Test Map")
        self.assertIsNone(map_instance.user_identifier)
        self.assertEqual(map_instance.description, "")
        self.assertEqual(map_instance.image_path, "")
        self.assertFalse(map_instance.initialised)
        self.assertFalse(map_instance.published)
        self.assertFalse(map_instance.promoted)
        self.assertIsNone(map_instance.owner)
        self.assertEqual(map_instance.collaboration_mode, CollaborationMode.VIEW)

    def test_init_with_all_parameters(self):
        collaboration_mode = CollaborationMode.EDIT
        map_instance = Map(
            identifier=2,
            name="Another Test Map",
            user_identifier=123,
            description="A description",
            image_path="/path/to/image.png",
            initialised=True,
            published=True,
            promoted=True,
            owner=True,
            collaboration_mode=collaboration_mode,
        )
        self.assertEqual(map_instance.identifier, 2)
        self.assertEqual(map_instance.name, "Another Test Map")
        self.assertEqual(map_instance.user_identifier, 123)
        self.assertEqual(map_instance.description, "A description")
        self.assertEqual(map_instance.image_path, "/path/to/image.png")
        self.assertTrue(map_instance.initialised)
        self.assertTrue(map_instance.published)
        self.assertTrue(map_instance.promoted)
        self.assertTrue(map_instance.owner)
        self.assertEqual(map_instance.collaboration_mode, CollaborationMode.EDIT)


if __name__ == "__main__":
    unittest.main()
