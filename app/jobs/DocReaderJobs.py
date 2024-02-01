
from worker.CelerySetup import celeryInstance
from time import sleep


class DocReaderJobs:

    @celeryInstance.task
    def addOne():
        return 'Sonucccc --- >Test--TEST'
