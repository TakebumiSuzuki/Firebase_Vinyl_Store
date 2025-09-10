import os

class BassConfig():
    SECRET_KEY= 'feaefgggwef93jf2u9ufn2efeafa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BassConfig):
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
    TESTING = False
    DEBUG = True

class ProductionConfig(BassConfig):
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
    TESTING = False
    DEBUG = False

class TestingConfig(BassConfig):
    TESTING = True
    DEBUG = False


configs_dic = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}