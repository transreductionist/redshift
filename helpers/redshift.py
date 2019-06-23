import psycopg2
from helpers.logger import log
from redshift_queries import s3_to_redshift

def get_redshift_connection_string(app):
    # TODO: replace endpoint with app.config
    connection_string = "dbname='{}' port='{}' user='{}' password='{}' host='{}'".format(
        app.config['REDSHIFT_DB'],
        app.config['REDSHIFT_PORT'],
        app.config['REDSHIFT_USER'],
        app.config['REDSHIFT_PASSWORD'],
        'redshift-cluster-1.c0vh9r6gf2go.us-east-1.redshift.amazonaws.com',
    )
    return connection_string

def redshift_connection(connection_string):
    connection = None
    log('Build psycopg2 Redshift connection.')
    try:
        connection = psycopg2.connect(connection_string)
    except psycopg2.OperationalError as error:
        log('psycopg2.OperationalError: {}'.format(error.args[0].rstrip()))
        log('Unable to connect to Redshift: exiting')
        exit(1)
    return connection


def get_redshift_cursor(connection):
    cursor = None
    try:
        cursor = connection.cursor()
    except AttributeError as error:
        log(error)
        exit(1)
    return cursor

def copy_s3_file_to_redshift(app, connection):
    redshift_query = s3_to_redshift(app)
    try:
        cursor.execute(redshift_query)
        log('Copy Command executed successfully')
    except:
        log('Failed to execute copy command: exiting')
        exit(1)
    connection.close()
