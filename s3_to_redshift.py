from helpers.application import create_app
from helpers.database import load_mysql
from helpers.database import reset_database
from helpers.logger import log
from helpers.redshift import copy_s3_file_to_redshift
from helpers.redshift import get_redshift_connection_string
from helpers.redshift import get_redshift_cursor
from helpers.redshift import redshift_connection
from helpers.save_s3_file import save_bytesio_to_s3


def save_csv_to_s3(app):
    reset_database()
    data_path = app.config['REDSHIFT_DATA_PATH']
    data, redshift_header = load_mysql(data_path, 'python_test.csv')
    save_bytesio_to_s3(data, redshift_header, 's3.csv')

def copy_s3_to_redshift(app):
    connection_string = get_redshift_connection_string(app)
    redshift_conn = redshift_connection(connection_string)
    redshift_cursor = get_redshift_cursor(redshift_conn)
    copy_s3_file_to_redshift(app, redshift_cursor)

redshift = create_app()

with redshift.app_context():
    log('Saving CSV file to AWS S3.')
    save_csv_to_s3(redshift)

    log('Copying CSV file to AWS Redshift')
    copy_s3_to_redshift(redshift)
