from celery import Celery
from confs import appName

celeryInstance = Celery(
    appName, broker='amqp://guest:guest@localhost:5672/', backend='mongodb://localhost:27017/')


def setupCelery(appInstance):
    # print('----------- [Creating Cellery] -----------')
    appInstance.config['result_backend'] = 'mongodb://localhost:27017/'
    appInstance.config['CELERY_broker_url'] = 'amqp://guest:guest@localhost:5672/'
    celeryInstance.conf.update(appInstance.config)
    return celeryInstance
