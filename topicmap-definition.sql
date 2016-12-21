CREATE TABLE IF NOT EXISTS member (
    topicmap_identifier INTEGER,
    identifier TEXT,
    role_spec TEXT,
    association_identifier_fk TEXT,
    PRIMARY KEY (topicmap_identifier, identifier)
);
CREATE INDEX IF NOT EXISTS member_1_index ON member (topicmap_identifier, association_identifier_fk);

CREATE TABLE IF NOT EXISTS attribute (
    topicmap_identifier INTEGER,
    identifier TEXT,
    parent_identifier_fk TEXT,
    name TEXT,
    value TEXT,
    data_type TEXT,
    scope TEXT,
    language TEXT,
    PRIMARY KEY (topicmap_identifier, identifier, parent_identifier_fk, name, scope)
);
CREATE INDEX IF NOT EXISTS attribute_1_index ON attribute (topicmap_identifier, name);
CREATE INDEX IF NOT EXISTS attribute_2_index ON attribute (topicmap_identifier, identifier);
CREATE INDEX IF NOT EXISTS attribute_3_index ON attribute (topicmap_identifier, parent_identifier_fk, language);
CREATE INDEX IF NOT EXISTS attribute_4_index ON attribute (topicmap_identifier, parent_identifier_fk);
CREATE INDEX IF NOT EXISTS attribute_5_index ON attribute (topicmap_identifier, parent_identifier_fk, name);

CREATE TABLE IF NOT EXISTS occurrence (
    topicmap_identifier INTEGER,
    identifier TEXT,
    instance_of TEXT,
    scope TEXT,
    resource_ref TEXT,
    resource_data BLOB,
    topic_identifier_fk TEXT,
    language TEXT,
    PRIMARY KEY (topicmap_identifier, identifier)
);
CREATE INDEX IF NOT EXISTS occurrence_1_index ON occurrence (topicmap_identifier, topic_identifier_fk, scope, language);
CREATE INDEX IF NOT EXISTS occurrence_2_index ON occurrence (topicmap_identifier, topic_identifier_fk, instance_of, language);
CREATE INDEX IF NOT EXISTS occurrence_3_index ON occurrence (topicmap_identifier, topic_identifier_fk);

CREATE TABLE IF NOT EXISTS topicref (
    topicmap_identifier INTEGER,
    topic_ref TEXT,
    member_identifier_fk TEXT,
    PRIMARY KEY (topicmap_identifier, topic_ref, member_identifier_fk)
);

CREATE TABLE IF NOT EXISTS topic (
    topicmap_identifier INTEGER,
    identifier TEXT,
    instance_of TEXT,
    scope TEXT,
    PRIMARY KEY (topicmap_identifier, identifier)
);
CREATE INDEX IF NOT EXISTS topic_1_index ON topic (topicmap_identifier, instance_of);
CREATE INDEX IF NOT EXISTS topic_2_index ON topic (topicmap_identifier, scope);
CREATE INDEX IF NOT EXISTS topic_3_index ON topic (topicmap_identifier, identifier, scope);
CREATE INDEX IF NOT EXISTS topic_4_index ON topic (topicmap_identifier, identifier, instance_of);

CREATE TABLE IF NOT EXISTS basename (
    topicmap_identifier INTEGER,
    identifier TEXT,
    name TEXT,
    topic_identifier_fk TEXT,
    language TEXT,
    PRIMARY KEY (topicmap_identifier, identifier, name, language)
);
CREATE INDEX IF NOT EXISTS basename_1_index ON basename (topicmap_identifier, topic_identifier_fk);
CREATE INDEX IF NOT EXISTS basename_2_index ON basename (topicmap_identifier, language, name);
CREATE INDEX IF NOT EXISTS basename_3_index ON basename (topicmap_identifier, topic_identifier_fk, language);

CREATE TABLE IF NOT EXISTS story (
    identifier INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    topicmap_identifier_fk INTEGER,
    scene_identifier_fk TEXT /* Start scene (topic) identifier. */
);
CREATE INDEX IF NOT EXISTS story_1_index ON story (identifier, topicmap_identifier_fk);
CREATE INDEX IF NOT EXISTS story_2_index ON story (identifier, topicmap_identifier_fk, scene_identifier_fk);