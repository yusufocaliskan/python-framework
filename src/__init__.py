
from flask_cors import CORS
from src.routes.v1 import Routes
from worker.CelerySetup import setupCelery


class Application:

    # Holds db
    dbConnector = None

    # Application Instance
    appInstance = None

    def setup(self, appInstance):

        self.appInstance = appInstance

        # Cors
        CORS(self.appInstance)

        setupCelery(appInstance)

        # Routes
        Routes(self.appInstance)

        return self.appInstance
