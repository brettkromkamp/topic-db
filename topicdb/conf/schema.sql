-- ************ TOPIC ************
CREATE TABLE IF NOT EXISTS topic (
    identifier TEXT NOT NULL PRIMARY KEY,
    instance_of TEXT NOT NULL,
    scope TEXT
);
CREATE INDEX topic_1_index ON topic(instance_of);
CREATE INDEX topic_2_index ON topic(scope);
CREATE INDEX topic_3_index ON topic(instance_of, scope);


-- ************ BASENAME ************
CREATE TABLE IF NOT EXISTS basename (
    identifier TEXT NOT NULL PRIMARY KEY,
    topic_identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL
);
CREATE UNIQUE INDEX basename_1_index ON basename(topic_identifier, name);
CREATE INDEX basename_2_index ON basename(topic_identifier);
CREATE INDEX basename_3_index ON basename(topic_identifier, scope);
CREATE INDEX basename_4_index ON basename(topic_identifier, scope, language);


-- ************ MEMBER ************
CREATE TABLE IF NOT EXISTS member (
    identifier TEXT NOT NULL PRIMARY KEY,
    association_identifier TEXT NOT NULL,
    src_role_spec TEXT NOT NULL,
    src_topic_ref TEXT NOT NULL,
    dest_role_spec TEXT NOT NULL,
    dest_topic_ref TEXT NOT NULL
);
CREATE UNIQUE INDEX member_1_index ON member(association_identifier, src_role_spec, src_topic_ref, dest_role_spec, dest_topic_ref);


-- ************ OCCURRENCE ************
CREATE TABLE IF NOT EXISTS occurrence (
    identifier TEXT NOT NULL PRIMARY KEY,
    topic_identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    resource_ref TEXT NOT NULL,
    resource_data BLOB,    
    scope TEXT NOT NULL,
    language TEXT NOT NULL
);
CREATE INDEX occurrence_1_index ON occurrence(topic_identifier);
CREATE INDEX occurrence_2_index ON occurrence(topic_identifier, scope, language);
CREATE INDEX occurrence_3_index ON occurrence(topic_identifier, instance_of, scope, language);


-- ************ ATTRIBUTE ************
CREATE TABLE IF NOT EXISTS attribute (
    identifier TEXT NOT NULL PRIMARY KEY,
    entity_identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    data_type TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL
);
CREATE UNIQUE INDEX attribute_1_index ON attribute(entity_identifier, name, scope, language);
CREATE INDEX attribute_2_index ON attribute(entity_identifier);
CREATE INDEX attribute_3_index ON attribute(entity_identifier, language);
CREATE INDEX attribute_4_index ON attribute(entity_identifier, scope);
CREATE INDEX attribute_5_index ON attribute(entity_identifier, scope, language);


-- ************ TOPIC MAP ************
CREATE TABLE IF NOT EXISTS map (
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT,
    creation_datetime TEXT,
    modification_datetime TEXT
);


-- ************ FULL-TEXT SEARCH ************
CREATE VIRTUAL TABLE text USING fts5 (
    occurrence_identifier,
    resource_data
);