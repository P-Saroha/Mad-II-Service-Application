from flask import Flask, render_template
# from flask_login import login_required
from Backend.config import LocalDevelopmentConfig
from Backend.models import db
from flask_jwt_extended import JWTManager
import flask_excel as excel
from flask_cors import CORS
from flask_caching import Cache
from Backend.celery.celery_factory import celery_init_app
import os

def createApp():
    app = Flask(__name__, template_folder='Frontend', static_folder='Frontend', static_url_path='/static')

    app.config.from_object(LocalDevelopmentConfig)

    # model init
    db.init_app(app)

    # Enable CORS for Vercel frontend
    CORS(app, origins=["https://mad-ii-service-application.vercel.app"], supports_credentials=True)

    # init cache
    cache = Cache(app)
    app.cache = cache

    jwt = JWTManager(app)

    app.app_context().push()

    # flask-restful init
    from Backend.resources import api
    api.init_app(app)

    return app

# Initialize Flask app
app = createApp()

# Initialize Celery
celery_app = celery_init_app(app)

# Load other modules
import Backend.create_initial_data
import Backend.routes
import Backend.celery.celery_schedule

# Init Excel handling
excel.init_excel(app)

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created if they don't exist

    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally
    app.run(host="0.0.0.0", port=port, debug=True)
