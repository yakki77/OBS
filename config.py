#!/usr/bin/env python
# coding=utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'obs secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://localhost:3306/task'

class TestingConfig(Config): 
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://localhost:3306/task'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost:3306/obs'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
