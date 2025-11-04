from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_restful import Api
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

api = Api(app)

def create_database():
    with app.app_context():
        db.create_all()

from . import models
from .views import views
app.register_blueprint(views)

create_database()
