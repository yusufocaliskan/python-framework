
import os

from src.constants.devConfigs import DevelopmentConfigs
# from src.constants.prodConfigs import ProductionConfigs

baseDir = os.path.abspath(os.path.dirname(__file__))

appName = 'GptVerseDocReader'
appConfigs = DevelopmentConfigs()

# Load production configs on production
# if (os.environ.get('FLASK_ENV') == 'production'):
#     appConfigs = ProductionConfigs()
