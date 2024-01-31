from flask import Flask
from flask_cors import CORS
from app.routes.v1 import Routes
from celery import Celery

from confs import appConfigs


class Application:

    # Holds db
    dbConnector = None

    # Application Instance
    appInstance = None

    celeryInstance = None

    def start(self):

        # setup the app
        self.appInstance = Flask(__name__)

        # Cors
        CORS(self.appInstance)

        # Routes
        Routes(self.appInstance)

        # configs
        self.appInstance.config['CELERY_RESULT_BACKEND'] = appConfigs.celery_result_backend
        self.appInstance.config['CELERY_BROKER_URL'] = appConfigs.celery_broker_url

        # Celery
        self.initialCelery()

        # Run the server
        self.appInstance.run(host=appConfigs.host, port=appConfigs.port,
                             debug=appConfigs.debug)

    def initialCelery(self):
        self.celeryInstance = Celery(
            self.appInstance.name, broker=appConfigs.celery_broker_url)

        # update the celery confs
        self.celeryInstance.conf.update(self.appInstance.config)
