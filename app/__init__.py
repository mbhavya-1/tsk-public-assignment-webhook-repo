from flask import Flask

from app.webhook.routes import webhook

from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # registering all the blueprints
    CORS(app)
    app.register_blueprint(webhook)

    @app.route('/')
    def hello_world():
        return "<p>Hello, World!</p>"
    
    return app
