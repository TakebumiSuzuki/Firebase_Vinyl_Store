import os

class BassConfig():
    SECRET_KEY= 'feaefgggwef93jf2u9ufn2efeafa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BassConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
    TESTING = False
    DEBUG = True

class ProductionConfig(BassConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
    TESTING = False
    DEBUG = False

class TestingConfig(BassConfig):
    # docker-compose.test.ymlにおいて、指定される
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')
    TESTING = True
    DEBUG = False


configs_dic = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}