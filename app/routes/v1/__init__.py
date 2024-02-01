
from .DocReaderRoutes import doc_read_routes
from .LanguageTutorRoutes import language_tutor_routes
from .HomeRoutesRoutes import home_routes


class Routes:
    def __init__(self, app):
        app.register_blueprint(home_routes)
        app.register_blueprint(doc_read_routes)
        app.register_blueprint(language_tutor_routes)
