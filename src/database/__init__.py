

from src.database.drivers import DatabaseDriver
# from src.database.seeds.clients import generateAClient


class Database:
    dbInstance = None

    @staticmethod
    def getDBInstance():
        return DatabaseDriver().driver

    # runs the seeds
    # @staticmethod
    # def sowTheSeed():
    #     generateAClient(dbInstance=self.getDBInstance())
    #     generateAClient(dbInstance=self.getDBInstance())
    #     generateAClient(dbInstance=self.getDBInstance())
