from flask import Flask
from app.routes import Routes


class Application:
    app = Flask(__name__)

    dbConnector = ''

    def __init__(self, connector):
        self.dbConnector = connector()

    def start(self):

        # Load the routes
        Routes(self.app)

        # Start the app
        return self.app.run()
