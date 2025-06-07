from flask import Flask , render_template
# from flask_login import login_required
from Backend.config import LocalDevelopmentConfig
from Backend.models import db
from flask_jwt_extended import JWTManager
import flask_excel as excel
from flask_cors import CORS
from flask_caching import Cache
from Backend.celery.celery_factory import celery_init_app

def createApp():
    app = Flask(__name__, template_folder='Frontend', static_folder='Frontend', static_url_path='/static')

    app.config.from_object(LocalDevelopmentConfig)

    # model init
    db.init_app(app)
    CORS(app, origins=["https://mad-ii-service-application.vercel.app"], supports_credentials=True)

    

    # init cache
    cache = Cache(app)
    

    jwt = JWTManager(app)

    app.cache = cache


    app.app_context().push()

    from Backend.resources import api
    # flask-restful init
    api.init_app(app)

    return app

app = createApp()

celery_app = celery_init_app(app)

import Backend.create_initial_data

import Backend.routes

import Backend.celery.celery_schedule

excel.init_excel(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created if they don't exist
    app.run(debug=True)
