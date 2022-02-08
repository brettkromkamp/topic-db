from datetime import datetime

from typedtree.tree import Tree
from typedtree.traversalmode import TraversalMode

from slugify import slugify

from topicdb.core.store.topicstore import TopicStore
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.models.association import Association

import os

MAP_IDENTIFIER = 1
USER_IDENTIFIER_1 = 1
SPACE = " "
TAB = "\t"
SPACES_PER_TAB = 4
UNIVERSAL_SCOPE = "*"
ROOT_TOPIC = "python"
IDENTIFIER = 0
NAME = 1
INSTANCE_OF = 2
TAGS = 3


class TopicImportError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def sibling_index(siblings, identifier):
    result = None
    for index, sibling in enumerate(siblings):
        if sibling.identifier == identifier:
            result = index
    return result


def normalize_topic_name(topic_identifier):
    return " ".join([word.capitalize() for word in topic_identifier.split("-")])


def create_tree():
    script_dir = os.path.dirname(__file__)
    data_file = "template.dat"  # Sample template
    abs_file_path = os.path.join(script_dir, data_file)
    topics_file = open(abs_file_path, "r")
    stack = {}
    for line in topics_file:
        normalized_tags = None
        index = int(line.count(SPACE) / SPACES_PER_TAB)
        topic_data = line.strip().split(";")
        if len(topic_data) < 1 or len(topic_data) > 4:
            raise TopicImportError("Invalid topic data")
        topic_identifier = slugify(str(topic_data[IDENTIFIER]))
        topic_instance_of = "topic"
        if len(topic_data) == 1:  # Only identifier provided
            topic_name = normalize_topic_name(topic_identifier)
        elif len(topic_data) == 2:  # Both identifier and name is provided
            topic_name = topic_data[NAME] if topic_data[NAME] else normalize_topic_name(topic_identifier)
        elif len(topic_data) == 3:  # Identifier, name and type (instance of) is provided
            topic_name = topic_data[NAME] if topic_data[NAME] else normalize_topic_name(topic_identifier)
            topic_instance_of = slugify(str(topic_data[INSTANCE_OF])) if topic_data[INSTANCE_OF] else "topic"
        # All parameters have been provided: identifier, name, type and one or more (comma-separated) tags
        else:
            topic_name = topic_data[NAME] if topic_data[NAME] else normalize_topic_name(topic_identifier)
            topic_instance_of = slugify(str(topic_data[INSTANCE_OF])) if topic_data[INSTANCE_OF] else "topic"
            normalized_tags = ",".join([slugify(str(tag)) for tag in topic_data[TAGS].split(",")])
        topic = Topic(topic_identifier, topic_instance_of, topic_name)
        if normalized_tags:
            tags_attribute = Attribute("tags", normalized_tags, topic.identifier, data_type=DataType.STRING)
            topic.add_attribute(tags_attribute)
        stack[index] = topic_identifier
        if index == 0:  # Root node
            tree.add_node(
                topic_identifier,
                node_type="identifier",
                edge_type="relationship",
                payload=topic,
            )
        else:
            tree.add_node(
                topic_identifier,
                parent_pointer=stack[index - 1],
                node_type="identifier",
                edge_type="relationship",
                payload=topic,
            )


def store_topic(store, topic):
    if not store.topic_exists(MAP_IDENTIFIER, topic.identifier):
        text_occurrence = Occurrence(
            instance_of="text",
            topic_identifier=topic.identifier,
            scope=UNIVERSAL_SCOPE,
            resource_data="Topic automatically created.",
        )
        timestamp = str(datetime.now())
        modification_attribute = Attribute(
            "modification-timestamp",
            timestamp,
            topic.identifier,
            data_type=DataType.TIMESTAMP,
        )
        # Persist objects to the topic store
        store.create_topic(MAP_IDENTIFIER, topic)
        # store.create_occurrence(MAP_IDENTIFIER, text_occurrence)  # Not sure if these topics should have auto-generated topic text
        store.create_attribute(MAP_IDENTIFIER, modification_attribute)
        # Persist tags, if any
        tags_attribute = topic.get_attribute_by_name("tags")
        if tags_attribute:
            for tag in tags_attribute.value.split(","):
                store.create_tag(MAP_IDENTIFIER, topic.identifier, tag)


def create_topics(store):
    for node in tree.traverse(ROOT_TOPIC, mode=TraversalMode.DEPTH):
        # Create the 'instance_of' topic if it doesn't already exist
        instance_of_topic = Topic(
            node.payload.instance_of,
            "topic",
            normalize_topic_name(node.payload.instance_of),
        )
        store_topic(store, instance_of_topic)

        # Create the actual node topic
        store_topic(store, node.payload)


def store_association(
    store,
    topic_map_identifier,
    src_topic_ref,
    src_role_spec,
    dest_topic_ref,
    dest_role_spec,
    instance_of="navigation",
):
    association = Association(
        instance_of=instance_of,
        scope=UNIVERSAL_SCOPE,
        src_topic_ref=src_topic_ref,
        dest_topic_ref=dest_topic_ref,
        src_role_spec=src_role_spec,
        dest_role_spec=dest_role_spec,
    )
    # Persist object to the topic store
    store.create_association(MAP_IDENTIFIER, association)


def create_associations(store):
    for node in tree.traverse(ROOT_TOPIC, mode=TraversalMode.DEPTH):
        if node.parent:
            siblings = tree.get_siblings(node.identifier)
            index = sibling_index(siblings, node.identifier)
            up_identifier = node.parent[0]
            down_identifier = node.identifier
            previous_identifier = siblings[index - 1].identifier
            next_identifier = node.identifier
            store_association(
                store,
                down_identifier,
                "child",
                up_identifier,
                "parent",
                "association",
            )
            if index == 0:  # First sibling
                store_association(
                    store,
                    down_identifier,
                    "down",
                    up_identifier,
                    "up",
                )
            elif index == len(siblings) - 1:  # Last sibling
                store_association(
                    store,
                    down_identifier,
                    "topic",
                    up_identifier,
                    "up",
                )
                store_association(
                    store,
                    previous_identifier,
                    "previous",
                    next_identifier,
                    "next",
                )
            else:  # In-between siblings
                store_association(
                    store,
                    previous_identifier,
                    "previous",
                    next_identifier,
                    "next",
                )


# ================================================================================
if __name__ == "__main__":
    store = TopicStore("template.db")
    store.create_database()
    store.create_map(USER_IDENTIFIER_1, "Test Map", "A map for testing purposes.")
    store.populate_map(MAP_IDENTIFIER, USER_IDENTIFIER_1)

    tree = Tree()
    create_tree()
    print("-" * 80)
    tree.display(ROOT_TOPIC)
    print("-" * 80)
    for node in tree.traverse(ROOT_TOPIC, mode=TraversalMode.DEPTH):
        print(f"{node.payload.identifier} - {node.payload.instance_of} - {node.payload.first_base_name.name}")

    print("Creating topics...")
    create_topics(store)
    print("Topics created!")
    print("-" * 80)
    print("Creating associations...")
    create_associations(store)
    print("Associations created!")
    print("-" * 80)
    test_tree = store.get_topics_network(MAP_IDENTIFIER, ROOT_TOPIC, instance_ofs=["association"])
    test_tree.display(ROOT_TOPIC)
