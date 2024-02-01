
class DevelopmentConfigs:

    baseUrl = 'http://localhost:5000'
    port = 4040
    host = '0.0.0.0'
    debug = True

    # FIX: Use .env variables
    # -- Database
    database = 'mongo'
    dabase_url = 'mongodb://aih-worker-mongo:27017/'
    database_name = 'docReader'
    database_password = 'docReader'

    # -- celery
    celery_broker_url = 'redis://aih-worker-redis:6379/0'  # Then use RabbitMQ
    celery_result_backend = 'redis://aih-worker-redis:6379/0'
