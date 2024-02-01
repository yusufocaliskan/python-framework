
from flask_cors import CORS
from app.routes.v1 import Routes
# from worker.CellerySetup import setupCelery
from confs import appConfigs, appName
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
