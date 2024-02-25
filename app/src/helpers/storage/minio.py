import boto3
from botocore.exceptions import ClientError

class MinioClient:

    def __init__(self, endpoint_url, access_key, secret_key):
        self.s3_client = boto3.client('s3', 
                                      endpoint_url=endpoint_url,
                                      aws_access_key_id=access_key,
                                      aws_secret_access_key=secret_key)
    
    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            raise e

    def upload_file(self, bucket_name, file_name, file_path):
        try:
            self.s3_client.upload_file(file_path, bucket_name, file_name)
        except ClientError as e:
            raise e

    def download_file(self, bucket_name, file_name, download_path):
        try:
            self.s3_client.download_file(bucket_name, file_name, download_path)
        except ClientError as e:
            raise e

    def delete_file(self, bucket_name, file_name):
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        except ClientError as e:
            raise e

    def delete_bucket(self, bucket_name):
        try:
            self.s3_client.delete_bucket(Bucket=bucket_name)
        except ClientError as e:
            raise e
