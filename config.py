

class Config(object):
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite://:memory:'


class ProductionConfig(Config):
    SECRET_KEY = "\xe8\xe7\xe9\xc2T\xf5\x97\xfaTB^\xcc'O\xc8x"
    # DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    ENV = "development"
    SECRET_KEY = "\xd8\xe7\xe9\xc2T\xf5\x97\xfaTB^\xdc'O\xc8x"
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
