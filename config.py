import os


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    SECRET_KEY = "\xe8\xe7\xe9\xc2T\xf5\x97\xfaTB^\xcc'O\xc8x"


class DevelopmentConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    ENV = "development"
    SECRET_KEY = "\xd8\xe7\xe9\xc2T\xf5\x97\xfaTB^\xdc'O\xc8x"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
