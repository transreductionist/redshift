import os
from flask import Flask
from s3_web_storage import WebStorage
from helpers.flask_essentials import database

def create_app():
    redshift = Flask('redshift')
    configure_app(redshift)
    database.init_app(redshift)
    WebStorage.init_storage(redshift)
    return redshift

def configure_app(app):
    app.config.update({
        'SQLALCHEMY_TRACK_MODIFICATIONS': os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'],
        'SQLALCHEMY_DATABASE_URI': os.environ['SQLALCHEMY_DATABASE_URI'],
        'REDSHIFT_DATA_PATH': os.environ['REDSHIFT_DATA_PATH'],
        'REDSHIFT_DB': os.environ['REDSHIFT_DB'],
        'REDSHIFT_SCHEMA': os.environ['REDSHIFT_SCHEMA'],
        'REDSHIFT_TABLE': os.environ['REDSHIFT_TABLE'],
        'REDSHIFT_USER': os.environ['REDSHIFT_USER'],
        'REDSHIFT_PASSWORD': os.environ['REDSHIFT_PASSWORD'],
        'REDSHIFT_HOST': os.environ['REDSHIFT_HOST'],
        'REDSHIFT_PORT': os.environ['REDSHIFT_PORT'],
        'REDSHIFT_S3_FILE_PATH': os.environ['REDSHIFT_S3_FILE_PATH'],
        'AWS_REGION': os.environ['AWS_REGION'],
        'AWS_ACCESS_KEY': os.environ['AWS_ACCESS_KEY'],
        'AWS_SECRET_KEY': os.environ['AWS_SECRET_KEY'],
        'AWS_SIGNATURE_VERSION': os.environ['AWS_SIGNATURE_VERSION'],
        'AWS_BASE_URL': os.environ['AWS_BASE_URL'],
        'AWS_DEFAULT_PATH': os.environ['AWS_DEFAULT_PATH'],
        'AWS_DEFAULT_BUCKET': os.environ['AWS_DEFAULT_BUCKET'],
    })
