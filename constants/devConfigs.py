
class DevelopmentConfigs:

    baseUrl = 'http://localhost:5000'
    port = 5000
    host = '127.0.0.1'
    debug = True

    # -- Database
    database = 'mongo'
    dabase_url = 'mongodb://localhost:27017/'
    database_name = 'docReader'
    database_password = 'docReader'

    # -- celery
    celery_broker_url = 'redis://127.0.0.1:6379/0'  # Then use RabbitMQ
    celery_result_backend = 'redis://127.0.0.1:6379/0'
