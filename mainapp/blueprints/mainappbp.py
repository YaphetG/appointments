from flask import Blueprint,current_app,g
import sqlite3

main_app_bp = Blueprint('main_app_bp',__name__)


def connect_db(app):
    """Connects to the specific database.
    @param app_instance the application we want to connect db to.
    app_instance should have database config set.
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db(app):
    """ Open new connection if connection not previously
    created. Connection should be one per application.
    """
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db(app)
    return g.sqlite_db

def init_db(app):
    """Initializes the database."""

    db = get_db(app)
    with current_app.open_resource('database.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()




@main_app_bp.route('/')
def index():
    return "Hi world"
