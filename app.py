from app import Application
from bin.MongoDBConnector import MongoDBConnector

if __name__ == '__main__':
    appInstace = Application(MongoDBConnector)
    appInstace.start()
