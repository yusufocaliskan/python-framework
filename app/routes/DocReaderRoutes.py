
from flask import Blueprint

from app.controllers.DocReaderController import DockReaderController


doc_read_routes = Blueprint(
    'doc_read_routes', __name__, url_prefix='/doc-reader/')


docController = DockReaderController()


@doc_read_routes.route('/upload-files', methods=['GET'])
def uploadFiles():
    # -------- To upload new file
    return docController.uploadFiles()


@doc_read_routes.route('/ask-question', methods=['GET'])
def askQuestion():
    # -------- To upload new file
    return docController.askQuestion()
