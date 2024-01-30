
from flask import jsonify

from libs.DocReaderAI import DocReaderAI


class DockReaderController():

    def uploadFiles(self):
        docAI = DocReaderAI()
        print('DOCAU---:', docAI)

        return jsonify({'message': 'FromClasss Uploaddinggg'})
