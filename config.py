import os


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "\xe8\xe7\xe9\xc2T\xf5\x97\xfaTB^\xcc'O\xc8x"
    DATABASE = 'database.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


class DevelopmentConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    ENV = "development"
    SECRET_KEY = "\xd8\xe7\xe9\xc2T\xf5\x97\xfaTB^\xdc'O\xc8x"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestingConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
