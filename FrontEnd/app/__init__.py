<<<<<<< HEAD
# app/__init__.py

# third-party imports
import os

# flask Libraries
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from importlib import import_module

# local imports
from app.config import DevelopmentConfig

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True,
                template_folder=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'templates/'),
                static_folder=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'static/'))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        with open(os.path.join(os.getcwd(), 'instance/config.py'), 'x') as instance_config_file:
            instance_config_file.write('from os import path\n\n')
            instance_config_file.write('SECRET_KEY = \'p9Bv<3Eid9%$i01\' \n')
            instance_config_file.write('SQLALCHEMY_DATABASE_URI = \'sqlite:///\' + path.join(path.abspath('
                                       'path.dirname(__file__)), \'db.sqlite3\') \n')
    except OSError:
        pass

    app.config.from_object(DevelopmentConfig)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)
    Bootstrap(app)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint)

    from .api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint)

    # from .swagger import swagger as swagger_blueprint
    # app.register_blueprint(swagger_blueprint)

    @app.errorhandler(400)
    def bad_request(errors):
        return render_template('errors/400.html', title='Bad Request'), 400

    @app.errorhandler(401)
    def unauthorized(errors):
        return render_template('errors/400.html', title='unauthorized'), 401

    @app.errorhandler(403)
    def forbidden(errors):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(errors):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(errors):
        return render_template('errors/500.html', title='Server Error'), 500

    @app.errorhandler(502)
    def bad_gateway(errors):
        return render_template('errors/502.html', title='Server Error'), 502

    @app.errorhandler(503)
    def service_unavailable(errors):
        return render_template('errors/503.html', title='Server Error'), 503

    @app.errorhandler(504)
    def gateway_timeout(errors):
        return render_template('errors/504.html', title='Server Error'), 504

    return app

=======
# app/__init__.py

# third-party imports
import os

# flask Libraries
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from importlib import import_module

# local imports
from app.config import DevelopmentConfig

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True,
                template_folder=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'templates/'),
                static_folder=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'static/'))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        with open(os.path.join(os.getcwd(), 'instance/config.py'), 'x') as instance_config_file:
            instance_config_file.write('from os import path\n\n')
            instance_config_file.write('SECRET_KEY = \'p9Bv<3Eid9%$i01\' \n')
            instance_config_file.write('SQLALCHEMY_DATABASE_URI = \'sqlite:///\' + path.join(path.abspath('
                                       'path.dirname(__file__)), \'db.sqlite3\') \n')
    except OSError:
        pass

    app.config.from_object(DevelopmentConfig)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)
    Bootstrap(app)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint)

    from .api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint)

    # from .swagger import swagger as swagger_blueprint
    # app.register_blueprint(swagger_blueprint)

    @app.errorhandler(400)
    def bad_request(errors):
        return render_template('errors/400.html', title='Bad Request'), 400

    @app.errorhandler(401)
    def unauthorized(errors):
        return render_template('errors/400.html', title='unauthorized'), 401

    @app.errorhandler(403)
    def forbidden(errors):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(errors):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(errors):
        return render_template('errors/500.html', title='Server Error'), 500

    @app.errorhandler(502)
    def bad_gateway(errors):
        return render_template('errors/502.html', title='Server Error'), 502

    @app.errorhandler(503)
    def service_unavailable(errors):
        return render_template('errors/503.html', title='Server Error'), 503

    @app.errorhandler(504)
    def gateway_timeout(errors):
        return render_template('errors/504.html', title='Server Error'), 504

    return app

>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
