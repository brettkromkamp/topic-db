from topicdb.core.store.ontologymode import OntologyMode

from slugify import slugify

from topicdb.core.store.topicstore import TopicStore
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.models.association import Association
from topicdb.core.topicdberror import TopicDbError

import pypff


MAP_IDENTIFIER = 1
USER_IDENTIFIER_1 = 1
PERSIST_TO_TOPICMAP = True


class EmailImportError(Exception):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


def normalize_name(topic_name: str) -> str:
    return " ".join([word.capitalize() for word in topic_name.strip().split(" ")])


def create_type_topics(store: TopicStore) -> None:
    topics = {
        "email-folder": "Email Folder",
        "email-sender": "Email Sender",
        "email-message": "Email Message",
    }
    if PERSIST_TO_TOPICMAP:
        for k, v in topics.items():
            topic = Topic(identifier=k, instance_of="topic", name=v)
            store.create_topic(MAP_IDENTIFIER, topic, OntologyMode.LENIENT)


def populate_topic_map(file_name: str, store: TopicStore) -> None:
    pst = pypff.file()
    pst.open(file_name)
    root = pst.get_root_folder()
    messages = parse_folder(root)

    folders = []
    senders = []
    message_count = 1

    if messages:
        for message in messages:

            try:
                # Create folder topic
                folder_topic_identifier = slugify(message["folder"])
                if folder_topic_identifier not in folders:
                    folders.append(folder_topic_identifier)
                    folder_topic_name = normalize_name(message["folder"])

                    if PERSIST_TO_TOPICMAP:
                        folder_topic = Topic(
                            folder_topic_identifier, instance_of="email-folder", name=folder_topic_name
                        )
                        store.create_topic(MAP_IDENTIFIER, folder_topic)

                        # Tagging
                        store.create_tag(MAP_IDENTIFIER, folder_topic_identifier, "email-folder-tag")

                # Create sender topic
                sender_topic_identifier = slugify(message["sender"])
                if sender_topic_identifier not in senders:
                    senders.append(sender_topic_identifier)
                    sender_topic_name = normalize_name(message["sender"])

                    if PERSIST_TO_TOPICMAP:
                        sender_topic = Topic(
                            sender_topic_identifier, instance_of="email-sender", name=sender_topic_name
                        )
                        store.create_topic(MAP_IDENTIFIER, sender_topic)

                        # Tagging
                        store.create_tag(MAP_IDENTIFIER, sender_topic_identifier, "email-sender-tag")

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
                    message_topic = Topic(
                        message_topic_identifier, instance_of="email-message", name=message_topic_name
                    )
                    store.create_topic(MAP_IDENTIFIER, message_topic)
                    store.create_attribute(MAP_IDENTIFIER, date_time_attribute)

                # TODO: Create associations between the message topic and the sender and folder topics, respectively

                # TODO: Extract the message's (plain-text) body and attach it to the message topic as a text occurrence
            except (OSError, TypeError, TopicDbError) as error:
                print(f"Error: Unable to process message. Message will be skipped.")
                continue


def parse_folder(folder):
    messages = []
    for folder in folder.sub_folders:
        if folder.number_of_sub_folders:
            messages += parse_folder(folder)
        for sub_message in folder.sub_messages:
            message = None
            try:
                message = {
                    "folder": folder.name,
                    "subject": sub_message.subject,
                    "sender": sub_message.sender_name,
                    "datetime": sub_message.client_submit_time,
                    "body": sub_message.plain_text_body,
                }
            except OSError as error:
                print(f"Error: Unable to parse message. Folder name: {folder.name}, Subject: {sub_message.subject}.")
                message = {
                    "folder": folder.name,
                    "subject": sub_message.subject,
                    "sender": sub_message.sender_name,
                    "datetime": sub_message.client_submit_time,
                    "body": "Error: Unable to retrieve message body.",
                }
            if message:
                messages.append(message)
    return messages


def main() -> None:
    store = TopicStore("email.db")
    store.create_database()
    store.create_map(USER_IDENTIFIER_1, "Test Map", "A map for testing purposes.")
    store.populate_map(MAP_IDENTIFIER, USER_IDENTIFIER_1)

    print("Start...")
    create_type_topics(store)
    print("Populating the topic map")
    populate_topic_map("/home/brettk/Downloads/bandeja-de-entrada.pst", store)
    print("Done!")


if __name__ == "__main__":
    main()
