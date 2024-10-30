"""
constants.py. Part of the Contextualise (https://contextualise.dev) project.

October 30, 2024
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

NETWORK_MAX_DEPTH = 3
UNIVERSAL_SCOPE = "*"
DATABASE_PATH = "topics.db"
DDL = """
CREATE TABLE IF NOT EXISTS topic (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX IF NOT EXISTS topic_1_index ON topic (map_identifier);
CREATE INDEX IF NOT EXISTS topic_2_index ON topic (map_identifier, instance_of);
CREATE INDEX IF NOT EXISTS topic_3_index ON topic (map_identifier, identifier, scope);
CREATE INDEX IF NOT EXISTS topic_4_index ON topic (map_identifier, instance_of, scope);
CREATE INDEX IF NOT EXISTS topic_5_index ON topic (map_identifier, scope);
CREATE TABLE IF NOT EXISTS basename (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    topic_identifier TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX IF NOT EXISTS basename_1_index ON basename (map_identifier);
CREATE INDEX IF NOT EXISTS basename_2_index ON basename (map_identifier, topic_identifier);
CREATE INDEX IF NOT EXISTS basename_3_index ON basename (map_identifier, topic_identifier, scope);
CREATE INDEX IF NOT EXISTS basename_4_index ON basename (map_identifier, topic_identifier, scope, language);
CREATE TABLE IF NOT EXISTS member (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    association_identifier TEXT NOT NULL,
    src_topic_ref TEXT NOT NULL,
    src_role_spec TEXT NOT NULL,
    dest_topic_ref TEXT NOT NULL,
    dest_role_spec TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE UNIQUE INDEX IF NOT EXISTS member_1_index ON member(map_identifier, association_identifier, src_role_spec, src_topic_ref, dest_role_spec, dest_topic_ref);
CREATE TABLE IF NOT EXISTS occurrence (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT NOT NULL,
    resource_ref TEXT NOT NULL,
    resource_data BLOB,
    topic_identifier TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX IF NOT EXISTS occurrence_1_index ON occurrence (map_identifier);
CREATE INDEX IF NOT EXISTS occurrence_2_index ON occurrence (map_identifier, topic_identifier);
CREATE INDEX IF NOT EXISTS occurrence_3_index ON occurrence (map_identifier, topic_identifier, scope, language);
CREATE INDEX IF NOT EXISTS occurrence_4_index ON occurrence (map_identifier, topic_identifier, instance_of, scope, language);
CREATE TABLE IF NOT EXISTS attribute (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    entity_identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    data_type TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, entity_identifier, name, scope, language)
);
CREATE INDEX IF NOT EXISTS attribute_1_index ON attribute (map_identifier);
CREATE INDEX IF NOT EXISTS attribute_2_index ON attribute (map_identifier, identifier);
CREATE INDEX IF NOT EXISTS attribute_3_index ON attribute (map_identifier, entity_identifier);
CREATE INDEX IF NOT EXISTS attribute_4_index ON attribute (map_identifier, entity_identifier, language);
CREATE INDEX IF NOT EXISTS attribute_5_index ON attribute (map_identifier, entity_identifier, scope);
CREATE INDEX IF NOT EXISTS attribute_6_index ON attribute (map_identifier, entity_identifier, scope, language);
CREATE TABLE IF NOT EXISTS map (
    identifier INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    initialised BOOLEAN DEFAULT FALSE NOT NULL,
    published BOOLEAN DEFAULT FALSE NOT NULL,
    promoted BOOLEAN DEFAULT FALSE NOT NULL
);
CREATE INDEX IF NOT EXISTS map_1_index ON map (published);
CREATE INDEX IF NOT EXISTS map_2_index ON map (promoted);
CREATE TABLE IF NOT EXISTS user_map (
    user_identifier INT NOT NULL,
    map_identifier INT NOT NULL,
    owner BOOLEAN DEFAULT FALSE NOT NULL,
    collaboration_mode TEXT NOT NULL,
    PRIMARY KEY (user_identifier, map_identifier)
);
CREATE INDEX IF NOT EXISTS user_map_1_index ON user_map (owner);
CREATE VIRTUAL TABLE IF NOT EXISTS text USING fts5 (
    occurrence_identifier,
    resource_data
);
"""