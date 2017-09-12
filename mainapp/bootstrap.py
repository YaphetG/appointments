import os
import sqlite3

from flask import Flask,g
from config.config import DevelopmentConfig

app = Flask(__name__)

#loading basic configuration DEV from config module
app.config.from_object(DevelopmentConfig)

#adding database config
app.config.update(dict(
    DATABASE = os.path.join(app.root_path,'database.db')
))

#let enviromental configuration override previous once to allow dynamic
#configuration setups if set other wise silently fail

app.config.from_envvar('APP_CONFIG',silent = True)




def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """ Open new connection if connection not previously
    created. Connection should be one per application.
    """
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

#making sure everything is closed when app is destroyed
@app.teardown_appcontext
def close_db(error):
    """Closes  the database connection"""
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()

@app.route('/')
def show_entries():
    return "Hi world"
