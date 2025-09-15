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

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # フォーマッタの名前を 'standard' に変更（'default'でも良いですが、より具体的に）
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S' # 日時のフォーマットも指定できます
        },
    },
    'handlers': {
        # ハンドラの名前を 'console' に変更
        'console': {
            # StreamHandlerはPythonに標準で組み込まれているloggingモジュールの一部
            'class': 'logging.StreamHandler',
            'formatter': 'standard', # 上で定義した 'standard' フォーマッタを指定
            # StreamHandlerを使ってログを出力する。その出力先は、Flaskが提供する特別なwsgi_errors_streamというオブジェクトに任せる。これにより、開発環境ではコンソールに、本番環境ではサーバーのログに、自動的に振り分けてくれるようになる
            'stream': 'ext://flask.logging.wsgi_errors_stream'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'] # 'console' ハンドラを使うよう指定
    }
}