"""
TopicStore class. Part of the StoryTechnologies project.

February 24, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import psycopg2


class TopicStore:

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

        self.connection = None

    def open(self):
        connection_string = f"dbname='storytech' user='storytech' host={self.host}:{self.port} password={self.password}"
        self.connection = psycopg2.connect(connection_string)

    def close(self):
        if self.connection:
            self.connection.close()

    # ========== ASSOCIATION ==========

    def delete_association(self):
        pass

    def get_association(self):
        pass

    def get_association_groups(self):
        pass

    def get_associations(self):
        pass

    def set_association(self):
        pass

    # ========== ATTRIBUTE ==========

    def attribute_exists(self):
        pass

    def delete_attribute(self):
        pass

    def delete_attributes(self):
        pass

    def get_attribute(self):
        pass

    def get_attributes(self):
        pass

    def set_attribute(self):
        pass

    def set_attributes(self):
        pass

    # ========== METRIC ==========

    def get_metrics(self):
        pass

    # ========== OCCURRENCE ==========

    def delete_occurrence(self):
        pass

    def delete_occurrences(self):
        pass

    def get_occurrence(self):
        pass

    def get_occurrence_data(self):
        pass

    def get_occurrences(self):
        pass

    def occurrence_exists(self):
        pass

    def set_occurrence(self):
        pass

    def set_occurrence_data(self):
        pass

    # ========== TAG ==========

    def get_tags(self):
        pass

    def set_tag(self):
        pass

    def set_tags(self):
        pass

    # ========== TOPIC ==========

    def delete_topic(self):
        pass

    def get_related_topics(self):
        pass

    def get_topic(self):
        pass

    def get_topic_associations(self):
        pass

    def get_topic_identifiers(self):
        pass

    def get_topic_occurrences(self):
        pass

    def get_topics(self):
        pass

    def get_topics_hierarchy(self):
        pass

    def set_topic(self):
        pass

    def topic_exists(self):
        pass

    # ========== TOPICMAP ==========

    def delete_topicmap(self):
        pass

    def get_topicmap(self):
        pass

    def get_topicmaps(self):
        pass

    def set_topicmap(self):
        pass
