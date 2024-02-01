from worker.CelerySetup import setupCelery, celeryInstance
from flask import Flask
from app import Application
from confs import appConfigs, appName
from waitress import serve

# Setup the flasskk
appInstance = Flask(appName)
Application().setup(appInstance)


if __name__ == '__main__':
    # Dev = Run the server
    appInstance.run(host=appConfigs.host, port=appConfigs.port,
                    debug=appConfigs.debug)

    # Production = Run the server
    # serve(appInstance, host="0.0.0.0", port=appConfigs.port)
