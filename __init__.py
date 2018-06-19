from flask import Flask, g, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from celery import Celery
from werkzeug.utils import secure_filename
import sys, os
import celeryconfig


# upload config
UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}


app = Flask(__name__)
# mail config
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='psourabh9218@gmail.com',
    MAIL_PASSWORD='Temppass123@',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/fl'
db = SQLAlchemy(app)
mail = Mail(app)

# secret key - should not be here change later

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# celery config
app.config.update(
    CELERY_BROKER_URL='amqp://guest:guest@localhost:5672//',

)
celery = celeryconfig.make_celery(app)