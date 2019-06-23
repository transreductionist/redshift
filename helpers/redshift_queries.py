

def s3_to_redshift(app):

    table = app.config['REDSHIFT_TABLE']
    s3_path = app.config['REDSHIFT_S3_FILE_PATH']
    key = app.config['AWS_ACCESS_KEY']
    secret = app.config['AWS_SECRET_KEY']

    redshift_query = """copy '{}' from '{}'
        access_key_id '{}'
        secret_access_key {}
        region 'us-east-1'
        ignoreheader 1
        null as 'NA'
        removequotes
        delimiter ',';""".format(table, s3_path, key, secret)

    return redshift_query
