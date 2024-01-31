from pymongo import MongoClient
from confs import appConfigs


class MongoDBConnector:
    dbClient = None

    dbInstance = None

    def __init__(self):

        print('---------- [Tring to Connect MongoDB]------------')
        try:
            self.dbClient = MongoClient(appConfigs.dabase_url)
            self.dbInstance = self.dbClient[appConfigs.database_name]

            self.dbInstance.messages.insert_one({'text': 'New Test Here'})
            # self.dbInstance.admin.command('ping')
            print('---------- [Connection is success]------------')
        except Exception as e:

            print('---------- [The MongoDB Connection is failed ]------------')
            raise e
