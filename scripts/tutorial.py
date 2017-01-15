#!/usr/bin/env python

"""
Tutorial (command-line) script. Part of the StoryTechnologies project.

January 15, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.topic import Topic
from topicdb.core.models.association import Association

acme = Topic(identifier='acme', base_name='Acme Corporation')
jane = Topic(identifier='jane', base_name='Jane')
john = Topic(identifier='john', base_name='John')
peter = Topic(identifier='peter', base_name='Peter')
mary = Topic(identifier='mary', base_name='Mary')

association1 = Association(src_topic_ref='acme',
                           src_role_spec='employer',
                           dest_topic_ref='jane',
                           dest_role_spec='employee',
                           instance_of='employment')

