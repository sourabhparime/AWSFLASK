# python3
# @author:sourabh parime

import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # g is a special object that us unique for each request. Used to store data that might be accessed by multiple
        # functions during the request-response cycle. If get_db is called again within the request-response cylcle the
        # same g object is returned
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        # current_app points to the flask app that initiated the request.
        # the file "DATABASE" is a config file and will be initiated later.
        g.db.row_factory = sqlite3.Row
        # sqlite.Row returns the rows like dict's so that column names can be used
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    Initializes DB and runs schema file
    """
    db = get_db()

    with current_app.open_resource('static/schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))
