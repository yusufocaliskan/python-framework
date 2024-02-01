

from database.drivers import DatabaseDriver


class Database:
    dbInstance = None

    @staticmethod
    def getDBInstance():
        return DatabaseDriver().driver

    # runs the seeds
    @staticmethod
    def sowTheSeed():
        generateAClient(dbInstance=self.getDBInstance())
        generateAClient(dbInstance=self.getDBInstance())
        generateAClient(dbInstance=self.getDBInstance())
