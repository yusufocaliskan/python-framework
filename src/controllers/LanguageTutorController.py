
from flask import jsonify


class LanguageTutorController():

    def getMessages(self):
        return jsonify({'message': 'LanguageTutor controller'})
