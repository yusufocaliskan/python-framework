from flask import Flask
from waitress import serve

from src import Application

# Setup the flasskk
appInstance = Flask('GptVerseDocReader')
Application().setup(appInstance)


if __name__ == '__main__':

    # Dev = Run the server
    appInstance.run(host='0.0.0.0', port=3000, debug=True)

    # Production = Run the server
    # serve(appInstance, host="0.0.0.0", port=appConfigs.port)
