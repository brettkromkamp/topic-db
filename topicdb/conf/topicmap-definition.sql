CREATE SCHEMA IF NOT EXISTS topicdb;


CREATE TABLE IF NOT EXISTS topicdb.member (
    topicmap_identifier BIGINT NOT NULL,
    identifier TEXT NOT NULL,
    role_spec TEXT NOT NULL,
    association_identifier_fk TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, identifier)
);
CREATE INDEX member_1_index ON topicdb.member (topicmap_identifier, association_identifier_fk);


CREATE TABLE IF NOT EXISTS topicdb.attribute (
    topicmap_identifier BIGINT NOT NULL,
    identifier TEXT NOT NULL,
    parent_identifier_fk TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    data_type TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, parent_identifier_fk, name, scope, language)
);
CREATE INDEX attribute_1_index ON topicdb.attribute (topicmap_identifier, identifier);
CREATE INDEX attribute_2_index ON topicdb.attribute (topicmap_identifier, parent_identifier_fk);
CREATE INDEX attribute_3_index ON topicdb.attribute (topicmap_identifier, parent_identifier_fk, language);
CREATE INDEX attribute_4_index ON topicdb.attribute (topicmap_identifier, parent_identifier_fk, scope);
CREATE INDEX attribute_5_index ON topicdb.attribute (topicmap_identifier, parent_identifier_fk, scope, language);


CREATE TABLE IF NOT EXISTS topicdb.occurrence (
    topicmap_identifier BIGINT NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT NOT NULL,
    resource_ref TEXT NOT NULL,
    resource_data BYTEA,
    topic_identifier_fk TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, identifier)
);
CREATE INDEX occurrence_1_index ON topicdb.occurrence (topicmap_identifier, topic_identifier_fk);
CREATE INDEX occurrence_2_index ON topicdb.occurrence (topicmap_identifier, topic_identifier_fk, scope, language);
CREATE INDEX occurrence_3_index ON topicdb.occurrence (topicmap_identifier, topic_identifier_fk, instance_of, scope, language);


CREATE TABLE IF NOT EXISTS topicdb.topicref (
    topicmap_identifier BIGINT NOT NULL,
    topic_ref TEXT NOT NULL,
    member_identifier_fk TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, topic_ref, member_identifier_fk)
);
CREATE INDEX topicref_1_index ON topicdb.topicref (topicmap_identifier, member_identifier_fk);
CREATE INDEX topicref_2_index ON topicdb.topicref (topicmap_identifier, topic_ref);


CREATE TABLE IF NOT EXISTS topicdb.topic (
    topicmap_identifier BIGINT NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT,
    PRIMARY KEY (topicmap_identifier, identifier)
);
CREATE INDEX topic_1_index ON topicdb.topic (topicmap_identifier, identifier, scope);
CREATE INDEX topic_2_index ON topicdb.topic (topicmap_identifier, instance_of, scope);
CREATE INDEX topic_3_index ON topicdb.topic (topicmap_identifier, scope);


CREATE TABLE IF NOT EXISTS topicdb.basename (
    topicmap_identifier BIGINT NOT NULL,
    identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    topic_identifier_fk TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, identifier)
);
CREATE INDEX basename_1_index ON topicdb.basename (topicmap_identifier, topic_identifier_fk);


CREATE SEQUENCE topicdb.topic_map_id_sequence;

CREATE TABLE IF NOT EXISTS topicdb.topicmap (
    identifier BIGINT NOT NULL DEFAULT nextval('topicdb.topic_map_id_sequence'),
    title TEXT NOT NULL,
    description TEXT,
    topicmap_identifier_fk BIGINT,
    PRIMARY KEY (identifier)
);
CREATE INDEX topicmap_1_index ON topicdb.topicmap (identifier, topicmap_identifier_fk);

ALTER SEQUENCE topicdb.topic_map_id_sequence OWNED BY topicdb.topicmap.identifier;
