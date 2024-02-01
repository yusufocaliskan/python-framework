from worker.CelerySetup import setupCelery, celeryInstance
from flask import Flask
from app import Application
from confs import appConfigs, appName

# Setup the flasskk
appInstance = Flask(appName)
Application().setup(appInstance)


if __name__ == '__main__':
    # Run the server
    appInstance.run(host=appConfigs.host, port=appConfigs.port,
                    debug=appConfigs.debug)
