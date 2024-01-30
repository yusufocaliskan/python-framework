
from flask import jsonify

from app.DocReaderAI import DocReaderAI


class DockReaderController():

    def uploadFiles(self):
        docAI = DocReaderAI()

        return jsonify({'message': 'FromClasss Uploaddinggg'})
