from app.routes.v1 import Routes


class Application:

    # Holds db
    dbConnector = None

    # Application Instance
    appInstance = None

    def __init__(self,  appInstance):
        self.appInstance = appInstance

    def loadEnvironment(self):

        # Load the routes
        Routes(self.appInstance)
