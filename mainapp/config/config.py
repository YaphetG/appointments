
class BaseConfig(object):
    DEBUG = False
    TESTING = False



class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    USERNAME = 'dev'
    PASSWORD = 'default'
    SECRET_KEY = "devkeynotsosuper :'("


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    USERNAME = 'test'
    PASSWORD = 'default'
    SECRET_KEY = "testingkey"
