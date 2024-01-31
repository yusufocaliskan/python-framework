from app.routes.v1 import Routes


class Application:

    # Holds db
    dbConnector = ''

    # Application Instance
    appInstance = ''

    def __init__(self, dbConnector, appInstance):
        self.dbConnector = dbConnector()
        self.appInstance = appInstance

    def loadEnvironment(self):

        # Load the routes
        Routes(self.appInstance)

        # Start the app
        return self.appInstance
