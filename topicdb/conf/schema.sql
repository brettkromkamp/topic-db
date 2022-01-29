CREATE TABLE IF NOT EXISTS topic (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX topic_1_index ON topic (map_identifier);
CREATE INDEX topic_2_index ON topic (map_identifier, instance_of);
CREATE INDEX topic_3_index ON topic (map_identifier, identifier, scope);
CREATE INDEX topic_4_index ON topic (map_identifier, instance_of, scope);
CREATE INDEX topic_5_index ON topic (map_identifier, scope);
CREATE TABLE IF NOT EXISTS basename (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    topic_identifier TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX basename_1_index ON basename (map_identifier);
CREATE INDEX basename_2_index ON basename (map_identifier, topic_identifier);
CREATE INDEX basename_3_index ON basename (map_identifier, topic_identifier, scope);
CREATE INDEX basename_4_index ON basename (map_identifier, topic_identifier, scope, language);
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
CREATE UNIQUE INDEX member_1_index ON member(map_identifier, association_identifier, src_role_spec, src_topic_ref, dest_role_spec, dest_topic_ref);
CREATE TABLE IF NOT EXISTS occurrence (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT NOT NULL,
    resource_ref TEXT NOT NULL,
    resource_data BYTEA,
    topic_identifier TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX occurrence_1_index ON occurrence (map_identifier);
CREATE INDEX occurrence_2_index ON occurrence (map_identifier, topic_identifier);
CREATE INDEX occurrence_3_index ON occurrence (map_identifier, topic_identifier, scope, language);
CREATE INDEX occurrence_4_index ON occurrence (map_identifier, topic_identifier, instance_of, scope, language);
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
CREATE INDEX attribute_1_index ON attribute (map_identifier);
CREATE INDEX attribute_2_index ON attribute (map_identifier, identifier);
CREATE INDEX attribute_3_index ON attribute (map_identifier, entity_identifier);
CREATE INDEX attribute_4_index ON attribute (map_identifier, entity_identifier, language);
CREATE INDEX attribute_5_index ON attribute (map_identifier, entity_identifier, scope);
CREATE INDEX attribute_6_index ON attribute (map_identifier, entity_identifier, scope, language);
CREATE TABLE IF NOT EXISTS map (
    identifier INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    initialised BOOLEAN DEFAULT FALSE NOT NULL,
    published BOOLEAN DEFAULT FALSE NOT NULL,
    promoted BOOLEAN DEFAULT FALSE NOT NULL
);
CREATE INDEX map_1_index ON map (published);
CREATE INDEX map_2_index ON map (promoted);
CREATE TABLE IF NOT EXISTS user_map (
    user_identifier INT NOT NULL,
    map_identifier INT NOT NULL,
    owner BOOLEAN DEFAULT FALSE NOT NULL,
    collaboration_mode TEXT NOT NULL,
    PRIMARY KEY (user_identifier, map_identifier)
);
CREATE INDEX user_map_1_index ON user_map (owner);
CREATE VIRTUAL TABLE text USING fts5 (
    occurrence_identifier,
    resource_data
);