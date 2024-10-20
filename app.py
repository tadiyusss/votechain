from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "very_secret_key"
    from dashboard import dashboard
    from api import api

    app.register_blueprint(api)
    app.register_blueprint(dashboard)

    return app