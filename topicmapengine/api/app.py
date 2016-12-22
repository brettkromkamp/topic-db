"""
Connexion script. Part of the StoryTechnologies project.

December 22, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import connexion

from flask_cors import CORS


app = connexion.App(__name__)
CORS(app.app)
app.add_api('swagger.yaml')
application = app.app

if __name__ == '__main__':
    # Run standalone gevent server (http://www.gevent.org/index.html).
    app.run(port=8080, server='gevent')
