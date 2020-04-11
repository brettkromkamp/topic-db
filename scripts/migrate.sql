DROP INDEX topicdb.topicmap_1_index;
DROP INDEX topicdb.topicmap_2_index;

ALTER TABLE topicdb.topicmap
RENAME COLUMN shared TO published;

ALTER TABLE topicdb.topicmap 
DROP COLUMN user_identifier;

GRANT ALL PRIVILEGES ON TABLE topicdb.user_topicmap TO contextualise;
