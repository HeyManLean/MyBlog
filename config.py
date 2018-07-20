import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'SECRET_KEY'
    
    SQLCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True

    MAIL_HOSTNAME = 'smtp.bigbin.club'
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'bigbin@bigbin.club'
    MAIL_PASSWORD = 'BINbin13078313586'
    MAIL_SENDER = 'Mr.Lean <bigbin@bigbin.club>'

    DOWNLOAD_DIR = '/tmp/lean/images'

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'testing': TestingConfig
}