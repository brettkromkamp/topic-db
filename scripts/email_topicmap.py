from topicdb.core.store.ontologymode import OntologyMode

from slugify import slugify

from topicdb.core.store.topicstore import TopicStore
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.models.association import Association

import configparser
import os

import pypff


SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "../settings.ini")
USER_IDENTIFIER = 1
TOPIC_MAP_IDENTIFIER = 16

PERSIST_TO_TOPICMAP = True

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

database_username = config["DATABASE"]["Username"]
database_password = config["DATABASE"]["Password"]
database_name = config["DATABASE"]["Database"]
database_host = config["DATABASE"]["Host"]
database_port = config["DATABASE"]["Port"]


class EmailImportError(Exception):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


def normalize_name(topic_name: str) -> str:
    return " ".join([word.capitalize() for word in topic_name.strip().split(" ")])


def create_type_topics(topic_store: TopicStore) -> None:
    topics = {
        "email-folder": "Email Folder",
        "email-sender": "Email Sender",
        "email-message": "Email Message",
    }
    if PERSIST_TO_TOPICMAP:
        for k, v in topics.items():
            topic = Topic(identifier=k, instance_of="topic", name=v)
            topic_store.set_topic(TOPIC_MAP_IDENTIFIER, topic, OntologyMode.LENIENT)


def populate_topic_map(file_name: str, topic_store: TopicStore) -> None:
    pst = pypff.file()
    pst.open(file_name)
    root = pst.get_root_folder()
    messages = parse_folder(root)

    folders = []
    senders = []

    message_count = 1

    topic_store.open()

    if messages:
        for message in messages:

            # Create folder topic
            folder_topic_identifier = slugify(message["folder"])
            if folder_topic_identifier not in folders:
                folders.append(folder_topic_identifier)
                folder_topic_name = normalize_name(message["folder"])

                if PERSIST_TO_TOPICMAP:
                    folder_topic = Topic(folder_topic_identifier, instance_of="email-folder", name=folder_topic_name)
                    topic_store.set_topic(TOPIC_MAP_IDENTIFIER, folder_topic)

                    # Tagging
                    topic_store.set_tag(TOPIC_MAP_IDENTIFIER, folder_topic_identifier, "email-folder-tag")

            # Create sender topic
            sender_topic_identifier = slugify(message["sender"])
            if sender_topic_identifier not in senders:
                senders.append(sender_topic_identifier)
                sender_topic_name = normalize_name(message["sender"])

                if PERSIST_TO_TOPICMAP:
                    sender_topic = Topic(sender_topic_identifier, instance_of="email-sender", name=sender_topic_name)
                    topic_store.set_topic(TOPIC_MAP_IDENTIFIER, sender_topic)

                    # Tagging
                    topic_store.set_tag(TOPIC_MAP_IDENTIFIER, sender_topic_identifier, "email-sender-tag")

            # Create message topic
            message_topic_identifier = slugify(f"message-{message['datetime']}-{str(message_count).zfill(4)}")
            message_count += 1
            message_topic_name = normalize_name(f"Message {message['datetime']}")
            if PERSIST_TO_TOPICMAP:
                date_time_attribute = Attribute(
                    "date-time-timestamp",
                    message["datetime"],
                    message_topic_identifier,
                    data_type=DataType.TIMESTAMP,
                )
                # Persist objects to the topic store
                message_topic = Topic(message_topic_identifier, instance_of="email-message", name=message_topic_name)
                topic_store.set_topic(TOPIC_MAP_IDENTIFIER, message_topic)
                topic_store.set_attribute(TOPIC_MAP_IDENTIFIER, date_time_attribute)

            # TODO: Create associations between the message topic and the sender and folder topics, respectively

            # TODO: Extract the message's (plain-text) body and attach it to the message topic as a text occurrence


def parse_folder(folder):
    messages = []
    for folder in folder.sub_folders:
        if folder.number_of_sub_folders:
            messages += parse_folder(folder)
        for message in folder.sub_messages:
            messages.append(
                {
                    "folder": folder.name,
                    "subject": message.subject,
                    "sender": message.sender_name,
                    "datetime": message.client_submit_time,
                    "body": message.plain_text_body,
                }
            )
    return messages


def main() -> None:
    topic_store = TopicStore(
        database_username,
        database_password,
        host=database_host,
        port=database_port,
        dbname=database_name,
    )

    print("Start...")
    create_type_topics(topic_store)
    print("Populating the topic map")
    populate_topic_map("./scripts/archive-2012.pst", topic_store)
    print("Done!")


if __name__ == "__main__":
    main()
