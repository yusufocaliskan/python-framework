from celery import Celery
from confs import appConfigs, appName


celeryInstance = Celery(
    appName, broker=appConfigs.celery_broker_url, backend=appConfigs.celery_result_backend)


def setupCelery(appInstance):
    print('----------- [Creating Cellery] -----------')
    appInstance.config['result_backend'] = appConfigs.celery_result_backend
    appInstance.config['CELERY_broker_url'] = appConfigs.celery_broker_url
    celeryInstance.conf.result_expires = 60 * 5  # Save the result for 5min
    celeryInstance.conf.update(appInstance.config)
    return celeryInstance

