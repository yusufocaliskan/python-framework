from confs import appConfigs
from src.database.drivers.MongoDBConnector import MongoDBConnector


class DatabaseDriver:

    # default is mongo
    driver = None

    def __init__(self) -> None:
        if (appConfigs.database == 'mongo'):
            self.driver = MongoDBConnector().getInstance()
