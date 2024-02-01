
import os

from constants.devConfigs import DevelopmentConfigs
from constants.prodConfigs import ProductionConfigs

baseDir = os.path.abspath(os.path.dirname(__file__))

appName = 'GptVerseDocReader'
appConfigs = DevelopmentConfigs()

# Load production configs on production
# if (os.environ['FLASK_ENV'] == 'production'):
#     appConfigs = ProductionConfigs()
