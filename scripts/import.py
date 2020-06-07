from typedtree.tree import Tree  # type: ignore
from typedtree.traversalmode import TraversalMode

from datetime import datetime

import configparser
import os

from topicdb.core.store.topicstore import TopicStore
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.models.association import Association

SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "../settings.ini")
USER_IDENTIFIER = 1
TOPIC_MAP_IDENTIFIER = 3
SPACE = " "
TAB = "\t"
SPACES_PER_TAB = 4
UNIVERSAL_SCOPE = "*"
ROOT_TOPIC = "python-programming-language"

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

database_username = config["DATABASE"]["Username"]
database_password = config["DATABASE"]["Password"]
database_name = config["DATABASE"]["Database"]
database_host = config["DATABASE"]["Host"]
database_port = config["DATABASE"]["Port"]


def sibling_index(siblings, identifier):
    result = None
    for index, sibling in enumerate(siblings):
        if sibling.identifier == identifier:
            result = index
    return result


def create_tree():
    script_dir = os.path.dirname(__file__)
    data_file = "topics.dat"
    abs_file_path = os.path.join(script_dir, data_file)
    topics_file = open(abs_file_path, "r")
    stack = {}
    for line in topics_file:
        index = int(line.count(SPACE) / SPACES_PER_TAB)
        topic_identifier = line.strip()
        stack[index] = topic_identifier
        if index == 0:  # Root node
            tree.add_node(topic_identifier, node_type='identifier', edge_type='relationship')
        else:
            tree.add_node(
                topic_identifier, parent_pointer=stack[index - 1], node_type='identifier', edge_type='relationship')


def create_topic(store, topic_map_identifier, topic_identifier, topic_name):
    store.open()
    if not topic_store.topic_exists(topic_map_identifier, topic_identifier):
        topic = Topic(topic_identifier, 'topic', topic_name)
        text_occurrence = Occurrence(
            instance_of="text",
            topic_identifier=topic.identifier,
            scope=UNIVERSAL_SCOPE,
            resource_data="Topic automatically created.",
        )
        timestamp = str(datetime.now())
        modification_attribute = Attribute("modification-timestamp", timestamp, topic.identifier, data_type=DataType.TIMESTAMP)
        # Persist objects to the topic store
        topic_store.set_topic(topic_map_identifier, topic)
        topic_store.set_occurrence(topic_map_identifier, text_occurrence)
        topic_store.set_attribute(topic_map_identifier, modification_attribute)
    store.close()


def create_topics(store, topic_map_identifier):
    for node_identifier in tree.traverse(ROOT_TOPIC, mode=TraversalMode.DEPTH):
        normalised_topic_name = " ".join([
            word.capitalize()
            for word in node_identifier.split("-")
        ])
        create_topic(store, topic_map_identifier, node_identifier, normalised_topic_name)


def create_association(store, topic_map_identifier, src_topic_ref, src_role_spec, dest_topic_ref, dest_role_spec, instance_of="navigation"):
    store.open()
    association = Association(
        instance_of=instance_of,
        scope=UNIVERSAL_SCOPE,
        src_topic_ref=src_topic_ref,
        dest_topic_ref=dest_topic_ref,
        src_role_spec=src_role_spec,
        dest_role_spec=dest_role_spec,
    )
    # Persist object to the topic store
    store.set_association(topic_map_identifier, association)
    store.close()


def create_associations(store, topic_map_identifier):
    for identifier in tree.traverse(ROOT_TOPIC, mode=TraversalMode.DEPTH):
        node = tree[identifier]
        navigation = None
        if node.parent:
            siblings = tree.get_siblings(node.identifier)
            index = sibling_index(siblings, node.identifier)
            up_identifier = node.parent[0]
            down_identifier = identifier
            previous_identifier = siblings[index - 1].identifier
            next_identifier = identifier
            create_association(store, topic_map_identifier, down_identifier, "child", up_identifier, "parent", "association")
            if index == 0:  # First sibling
                create_association(store, topic_map_identifier, down_identifier, "down", up_identifier, "up")
            elif index == len(siblings) - 1:  # Last sibling
                create_association(store, topic_map_identifier, down_identifier, "topic", up_identifier, "up")
                create_association(store, topic_map_identifier, previous_identifier, "previous", next_identifier, "next")
            else:  # In-between siblings
                create_association(store, topic_map_identifier, previous_identifier, "previous", next_identifier, "next")


# ================================================================================
if __name__ == "__main__":
    topic_store = TopicStore(
        database_username,
        database_password,
        host=database_host,
        port=database_port,
        dbname=database_name,
    )
    tree = Tree()
    create_tree()
    print("-"*80)
    print("Creating topics...")
    create_topics(topic_store, TOPIC_MAP_IDENTIFIER)
    print("Topics created!")
    print("-"*80)
    print("Creating associations...")
    create_associations(topic_store, TOPIC_MAP_IDENTIFIER)
    print("Associations created!")
    print("-"*80)
    with topic_store:
        test_tree = topic_store.get_topics_network(TOPIC_MAP_IDENTIFIER, ROOT_TOPIC, instance_ofs=['association'])
        test_tree.display(ROOT_TOPIC)
