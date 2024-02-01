from celery import Celery
import os
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

celeryInstance = Celery('GptVerseDocReader', broker=CELERY_BROKER_URL,
                        backend=CELERY_RESULT_BACKEND)


def setupCelery(appInstance):
    print('----------- [Clreating Cellery] -----------')
    appInstance.config['result_backend'] = CELERY_RESULT_BACKEND
    appInstance.config['CELERY_broker_url'] = CELERY_BROKER_URL
    celeryInstance.conf.result_expires = 60 * 5  # Save the result for 5min
    celeryInstance.conf.update(appInstance.config)
    return celeryInstance
