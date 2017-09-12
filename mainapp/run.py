import os
import sqlite3

from flask import Flask,g,current_app
from config.config import DevelopmentConfig

from .blueprints import mainappbp



def register_blueprints(app):
    app.register_blueprint(mainappbp.main_app_bp)

#making sure everything is closed when app is destroyed
def create_teardown_context(app):
    """
    creates the teardown context for the app
    """
    @app.teardown_appcontext
    def close_db(error):
        """Closes  the database connection"""
        if hasattr(g,'sqlite_db'):
            g.sqlite_db.close()
def register_command(app):
    """
    registers cli command for the app
    """
#register a command for creating db
    @app.cli.command('initdb')
    def initdb_command():
        """Initializes the database."""
        mainappbp.init_db(app)




def create_app(config_class):
    """
    Creates a new application instance.
    @param config_class : configuration class to be used
    """
    app = Flask(__name__)

    #loading basic configuration DEV from config module
    app.config.from_object(config_class)

    #adding database config
    app.config.update(dict(
        DATABASE = os.path.join(app.root_path,'database.db')
        ))
    #let enviromental configuration override previous once to allow dynamic
    #configuration setups if set other wise silently fail
    app.config.from_envvar('APP_CONFIG',silent = True)
    create_teardown_context(app)
    register_command(app)
    register_blueprints(app)
    app.app_context()
    return app


app = create_app(DevelopmentConfig)
