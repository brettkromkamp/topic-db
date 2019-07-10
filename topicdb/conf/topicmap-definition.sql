/* ========== TOPICDB ========== */
create SCHEMA IF NOT EXISTS topicdb;


/* ========== MEMBER ========== */
create TABLE IF NOT EXISTS topicdb.member (
    topicmap_identifier INT NOT NULL,
    identifier TEXT NOT NULL,
    role_spec TEXT NOT NULL,
    association_identifier TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, identifier)
);
create INDEX member_1_index ON topicdb.member (topicmap_identifier);
create INDEX member_2_index ON topicdb.member (topicmap_identifier, association_identifier);


/* ========== ATTRIBUTE ========== */
create TABLE IF NOT EXISTS topicdb.attribute (
    topicmap_identifier INT NOT NULL,
    identifier TEXT NOT NULL,
    parent_identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    data_type TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, parent_identifier, name, scope, language)
);
create INDEX attribute_1_index ON topicdb.attribute (topicmap_identifier);
create INDEX attribute_2_index ON topicdb.attribute (topicmap_identifier, identifier);
create INDEX attribute_3_index ON topicdb.attribute (topicmap_identifier, parent_identifier);
create INDEX attribute_4_index ON topicdb.attribute (topicmap_identifier, parent_identifier, language);
create INDEX attribute_5_index ON topicdb.attribute (topicmap_identifier, parent_identifier, scope);
create INDEX attribute_6_index ON topicdb.attribute (topicmap_identifier, parent_identifier, scope, language);


/* ========== OCCURRENCE ========== */
create TABLE IF NOT EXISTS topicdb.occurrence (
    topicmap_identifier INT NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT NOT NULL,
    resource_ref TEXT NOT NULL,
    resource_data BYTEA,
    topic_identifier TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, identifier)
);
create INDEX occurrence_1_index ON topicdb.occurrence (topicmap_identifier);
create INDEX occurrence_2_index ON topicdb.occurrence (topicmap_identifier, topic_identifier);
create INDEX occurrence_3_index ON topicdb.occurrence (topicmap_identifier, topic_identifier, scope, language);
create INDEX occurrence_4_index ON topicdb.occurrence (topicmap_identifier, topic_identifier, instance_of, scope, language);


/* ========== TOPICREF ========== */
create TABLE IF NOT EXISTS topicdb.topicref (
    topicmap_identifier INT NOT NULL,
    topic_ref TEXT NOT NULL,
    member_identifier TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, topic_ref, member_identifier)
);
create INDEX topicref_1_index ON topicdb.topicref (topicmap_identifier);
create INDEX topicref_2_index ON topicdb.topicref (topicmap_identifier, member_identifier);
create INDEX topicref_3_index ON topicdb.topicref (topicmap_identifier, topic_ref);


/* ========== TOPIC ========== */
create TABLE IF NOT EXISTS topicdb.topic (
    topicmap_identifier INT NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT,
    PRIMARY KEY (topicmap_identifier, identifier)
);
create INDEX topic_1_index ON topicdb.topic (topicmap_identifier);
create INDEX topic_2_index ON topicdb.topic (topicmap_identifier, identifier, scope);
create INDEX topic_3_index ON topicdb.topic (topicmap_identifier, instance_of, scope);
create INDEX topic_4_index ON topicdb.topic (topicmap_identifier, scope);


/* ========== BASENAME ========== */
create TABLE IF NOT EXISTS topicdb.basename (
    topicmap_identifier INT NOT NULL,
    identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    topic_identifier TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (topicmap_identifier, identifier)
);
create INDEX basename_1_index ON topicdb.basename (topicmap_identifier);
create INDEX basename_2_index ON topicdb.basename (topicmap_identifier, topic_identifier);


/* ========== TOPICMAP ========== */
create sequence topicdb.topic_map_id_sequence;

create TABLE IF NOT EXISTS topicdb.topicmap (
    user_identifier INT NOT NULL,
    identifier INT NOT NULL DEFAULT nextval('topicdb.topic_map_id_sequence'),
    name TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    initialised BOOLEAN DEFAULT FALSE NOT NULL,
    shared BOOLEAN DEFAULT FALSE NOT NULL,
    promoted BOOLEAN DEFAULT FALSE NOT NULL,
    PRIMARY KEY (user_identifier, identifier)
);
create INDEX topicmap_1_index ON topicdb.topicmap (identifier);
create INDEX topicmap_2_index ON topicdb.topicmap (shared);
create INDEX topicmap_3_index ON topicdb.topicmap (promoted);

alter sequence topicdb.topic_map_id_sequence OWNED BY topicdb.topicmap.identifier;
