
from flask import Flask
from app import Application
from bin.MongoDBConnector import MongoDBConnector

flaskApp = Flask(__name__)

if __name__ == '__main__':
    appInstance = Application(connector=MongoDBConnector, app=flaskApp)
    appInstance.loadEnvironment()
    flaskApp.run(host="127.0.0.1", port=5000, debug=True)
