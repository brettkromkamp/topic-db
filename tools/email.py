from datetime import datetime

import pypff
from slugify import slugify
from topicdb.core.models.association import Association
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.store.ontologymode import OntologyMode
from topicdb.core.store.topicstore import TopicStore
from topicdb.core.topicdberror import TopicDbError

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
                message_topic_identifier = slugify(f"message-{message['submit_time']}-{str(message_count).zfill(4)}")
                message_count += 1
                message_topic_name = normalize_name(f"Message {message['submit_time']}")
                if PERSIST_TO_TOPICMAP:
                    date_time_attribute = Attribute(
                        "date-time-timestamp",
                        message["submit_time"],
                        message_topic_identifier,
                        data_type=DataType.TIMESTAMP,
                    )
                    # Persist objects to the topic store
                    message_topic = Topic(
                        message_topic_identifier, instance_of="email-message", name=message_topic_name
                    )
                    store.create_topic(MAP_IDENTIFIER, message_topic)
                    store.create_attribute(MAP_IDENTIFIER, date_time_attribute)

                    # TODO: Extract the message's (plain-text) body and attach it to the message topic as a text occurrence
                    message_body = message["body"] if message["body"] else ""
                    email_body_occurrence = Occurrence(
                        instance_of="text",
                        topic_identifier=message_topic.identifier,
                        resource_data=message_body,
                    )
                    store.create_occurrence(MAP_IDENTIFIER, email_body_occurrence)

                # Create associations between the message topic and the sender topic
                message_sender_association = Association(
                    instance_of="email-sender",
                    src_topic_ref=message_topic.identifier,
                    dest_topic_ref=sender_topic.identifier,
                )
                store.create_association(MAP_IDENTIFIER, message_sender_association)

                # Create associations between the message topic and the folder topic
                message_folder_association = Association(
                    instance_of="email-folder",
                    src_topic_ref=message_topic.identifier,
                    dest_topic_ref=folder_topic.identifier,
                )
                store.create_association(MAP_IDENTIFIER, message_folder_association)

            except (OSError, TypeError, TopicDbError) as error:
                print(f"Error: Unable to process message. Message will be skipped.")
                continue

        # Create associations to email-folder-tag and email-sender-tag topics, respectively
        folder_association = Association(
            src_topic_ref="home",
            dest_topic_ref="email-folder-tag",
        )
        store.create_association(MAP_IDENTIFIER, folder_association)
        sender_association = Association(
            src_topic_ref="home",
            dest_topic_ref="email-sender-tag",
        )
        store.create_association(MAP_IDENTIFIER, sender_association)


def parse_folder(folder):
    result = []
    for folder in folder.sub_folders:
        if folder.number_of_sub_folders:
            result += parse_folder(folder)
        for sub_message in folder.sub_messages:
            message = process_message(sub_message, folder)
            if message:
                result.append(message)
    return result


def process_message(message, folder):
    attachments = []
    total_attachment_size_bytes = 0
    if message.number_of_attachments > 0:
        for i in range(message.number_of_attachments):
            total_attachment_size_bytes = total_attachment_size_bytes + (message.get_attachment(i)).get_size()
            # attachments.append(
            #     ((message.get_attachment(i)).read_buffer((message.get_attachment(i)).get_size())).decode(
            #         "ascii", errors="ignore"
            #     )
            # )
    result = None
    try:
        result = {
            "folder": folder.name,
            "subject": message.subject,
            "sender": message.sender_name,
            "header": message.transport_headers,
            "body": message.plain_text_body,
            "creation_time": message.creation_time,
            "submit_time": message.client_submit_time,
            "delivery_time": message.delivery_time,
            "attachment_count": message.number_of_attachments,
            "total_attachment_size": total_attachment_size_bytes,
            # "attachments": attachments,
        }
    except OSError as error:
        print(f"Error: Unable to parse message. Folder name: {folder.name}, Subject: {message.subject}.")
        result = {
            "folder": folder,
            "subject": message.subject,
            "sender": message.sender_name,
            "header": message.transport_headers,
            "body": "Error: Unable to retrieve message body.",
            "creation_time": message.creation_time,
            "submit_time": message.client_submit_time,
            "delivery_time": message.delivery_time,
            "attachment_count": message.number_of_attachments,
            "total_attachment_size": total_attachment_size_bytes,
            # "attachments": attachments,
        }
    return result


def main() -> None:
    store = TopicStore("bandeja-de-entrada.db")
    store.create_database()
    store.create_map(USER_IDENTIFIER_1, "Email ETL", "A map resulting from an email ETL operation.")
    store.populate_map(MAP_IDENTIFIER, USER_IDENTIFIER_1)

    print("Start...")
    create_type_topics(store)
    print("Populating the topic map")
    populate_topic_map(
        "/home/brettk/Downloads/bandeja-de-entrada.pst", store
    )  # lpajvd-02.pst, carpetas-02.pst, bandeja-de-entrada.pst
    print("Done!")


if __name__ == "__main__":
    main()
