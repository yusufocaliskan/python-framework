
from flask import Blueprint
from app.controllers.DocReaderController import DockReaderController


docController = DockReaderController()
doc_read_routes = Blueprint(
    'doc_read_routes', __name__, url_prefix='/doc-reader/')


@doc_read_routes.route('/upload-files', methods=['GET'])
def uploadFiles():
    # -- To upload new file
    return docController.uploadFiles()


@doc_read_routes.route('/ask-question', methods=['GET'])
def askQuestion():
    # -- to ask a question to the agent
    # -- about uploaded files
    return docController.askQuestion()
