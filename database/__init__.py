

from database.drivers import DatabaseDriver


class Database:
    dbInstance = None

    @staticmethod
    def getDBInstance():
        return DatabaseDriver().driver
