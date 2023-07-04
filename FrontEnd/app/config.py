<<<<<<< HEAD
# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = True
    PORT = 80


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    DEVELOPMENT = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
    PORT = 80

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
=======
# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = True
    PORT = 80


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    DEVELOPMENT = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
    PORT = 80

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
