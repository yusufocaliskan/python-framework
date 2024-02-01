from database import Database


class DocReaderModel:

    dbInstance: None

    def __init__(self) -> None:
        self.dbInstance = Database.getDBInstance()

    def addMessage(self,  message, userId):
        self.dbInstance.todo.insert_one(
            {'tex=======t': 'Biraa----NewTRYTESTOOOO'})
