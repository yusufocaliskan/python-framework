
from flask import Blueprint

from app.controllers.LanguageTutorController import LanguageTutorController


language_tutor_routes = Blueprint(
    'language_tutor_routes', __name__, url_prefix='/language-tutor/')


# returns all messages
@language_tutor_routes.route('/get-messages', methods=['GET'])
def uploadFiles():
    return LanguageTutorController().getMessages()
