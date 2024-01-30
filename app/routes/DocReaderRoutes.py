
from flask import Blueprint

from app.controllers.DocReaderController import DockReaderController


doc_read_routes = Blueprint(
    'doc_read_routes', __name__, url_prefix='/doc-reader/')


@doc_read_routes.route('/upload-files', methods=['GET'])
def uploadFiles():
    return DockReaderController().uploadFiles()
