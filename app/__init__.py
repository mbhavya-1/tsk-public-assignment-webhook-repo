from flask import Flask

from app.webhook.routes import webhook

from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # CORS allows front-end and backend on different domains to interact
    CORS(app)

    # registering all the blueprints
    app.register_blueprint(webhook)

    
    return app
