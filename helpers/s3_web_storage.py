import os
import boto3
from botocore.client import Config


class WebStorage:
    @classmethod
    def init_storage(cls, current_app):
        cls.aws_access_key_id = current_app.config['AWS_ACCESS_KEY']
        cls.aws_secret_access_key = current_app.config['AWS_SECRET_KEY']
        cls.aws_bucket = current_app.config['AWS_DEFAULT_BUCKET']
        cls.aws_path = current_app.config['AWS_DEFAULT_PATH']
        cls.aws_base_url = current_app.config['AWS_BASE_URL']
        cls.aws_signature_version = current_app.config['AWS_SIGNATURE_VERSION']
        cls.s3 = boto3.resource(
            's3',
            aws_access_key_id=cls.aws_access_key_id,
            aws_secret_access_key=cls.aws_secret_access_key
        )

    @classmethod
    def save(cls, file_name, file_data, metadata=(None, None)):
        cls.s3.Bucket(cls.aws_bucket).put_object(
            Key=cls.aws_path + file_name,
            Body=file_data,
            Metadata={
                'file_source': metadata[0],
                'file_id': metadata[1],
            },
        )

    @classmethod
    def delete(cls, filename):
        cls.s3.Object(cls.aws_bucket, cls.aws_path + filename).delete()
        return True

    @classmethod
    def get_s3_path(cls):
        return '{}{}/{}'.format(cls.aws_base_url, cls.aws_bucket, cls.aws_path)

    @classmethod
    def get_list_of_bucket_files(cls):
        bucket = cls.s3.Bucket(cls.aws_bucket)
        files = []
        for obj in bucket.objects.filter(Prefix=cls.aws_path):
            if os.path.basename(obj.key) != '':
                files.append(os.path.basename(obj.key))

        return files

    @classmethod
    def get_bucket_file(cls, file_name, local_path):
        cls.s3.Bucket(cls.aws_bucket)\
            .download_file( cls.aws_path + file_name, local_path )
