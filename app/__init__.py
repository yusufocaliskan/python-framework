from app.routes import Routes


class Application:

    dbConnector = ''

    def __init__(self, connector, app):
        self.dbConnector = connector()

        self.app = app

    def loadEnvironment(self):

        # Load the routes
        Routes(self.app)

        # Start the app
        return self.app
