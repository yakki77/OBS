#!/usr/bin/env python
# coding=utf-8
from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


# def create_app(config_name):
#     app = Flask(__name__) 
#     app.config.from_object(config[config_name]) 
#     config[config_name].init_app(app)
    
#     db.init_app(app)
#     # attach routes and custom error pages here
#     return app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
# set mysql Anonymous account
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://localhost:3306/task'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
from app import views



