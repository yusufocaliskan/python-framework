from celery import Celery
from time import sleep
celeryInstance = Celery(
    'aih-worker-task', broker='amqp://guest:guest@localhost:5672/', backend='mongodb://localhost:27017/')


@celeryInstance.task
def add():
    sleep(15)
    return 'Heeeeee'


add()
