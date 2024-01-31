
from flask import Flask
from flask_cors import CORS
from app import Application
from confs import appConfigs

# setup the app
flaskApp = Flask(__name__)
CORS(flaskApp)
appInstance = Application(appInstance=flaskApp)
appInstance.loadEnvironment()


# -- Run  the server
if __name__ == '__main__':
    flaskApp.run(host=appConfigs.host, port=appConfigs.port,
                 debug=appConfigs.debug)
