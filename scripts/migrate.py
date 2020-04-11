import configparser
import os

import psycopg2.extras

SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "../settings.ini")

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

username = config["DATABASE"]["Username"]
password = config["DATABASE"]["Password"]
name = config["DATABASE"]["Database"]
host = config["DATABASE"]["Host"]
port = config["DATABASE"]["Port"]

connection = psycopg2.connect(dbname=name, user=username, password=password, host=host, port=port)

with connection, connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    cursor.execute("SELECT * FROM topicdb.topicmap")
    records = cursor.fetchall()
    for record in records:
        cursor.execute(
            "INSERT INTO topicdb.user_topicmap (user_identifier, topicmap_identifier, user_name, owner, collaboration_mode) VALUES (%s, %s, %s, %s, %s)",
            (record['user_identifier'],
             record['identifier'],
             '',
             True,
             'edit'))
