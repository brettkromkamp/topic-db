"""
setup.py file. Part of the StoryTechnologies project.

December 21, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from setuptools import setup, find_packages

setup(name='topic_db',
      version='0.1.0',
      description='Topic map-based graph database',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Topic :: Database :: Database Engines/Servers',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='topic map, graph database, nosql, semantic',
      url='https://github.com/brettkromkamp/topicmap_engine',
      author='Brett Alistair Kromkamp',
      author_email='brett.kromkamp@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'connexion', 'flask-cors', 'gevent', 'python-slugify'
      ],
      include_package_data=True,
      zip_safe=False)
