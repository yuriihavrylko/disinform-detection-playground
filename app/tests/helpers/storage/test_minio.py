import pytest
from src.helpers.storage.minio import MinioClient

@pytest.fixture
def minio_client():
    endpoint_url = 'http://localhost:9000'
    access_key = 'minio_access_key'
    secret_key = 'minio_secret_key'
    return MinioClient(endpoint_url, access_key, secret_key)

def test_create_bucket(mocker, minio_client):
    mock_s3 = mocker.patch.object(minio_client.s3_client, 'create_bucket')
    minio_client.create_bucket('testbucket')
    mock_s3.assert_called_once_with(Bucket='testbucket')

def test_upload_file(mocker, minio_client):
    mock_upload_file = mocker.patch.object(minio_client.s3_client, 'upload_file')
    minio_client.upload_file('testbucket', 'test.txt', '/path/to/test.txt')
    mock_upload_file.assert_called_once_with('/path/to/test.txt', 'testbucket', 'test.txt')

def test_download_file(mocker, minio_client):
    mock_download_file = mocker.patch.object(minio_client.s3_client, 'download_file')
    minio_client.download_file('testbucket', 'test.txt', '/path/to/downloaded/test.txt')
    mock_download_file.assert_called_once_with('testbucket', 'test.txt', '/path/to/downloaded/test.txt')

def test_delete_file(mocker, minio_client):
    mock_delete_object = mocker.patch.object(minio_client.s3_client, 'delete_object')
    minio_client.delete_file('testbucket', 'test.txt')
    mock_delete_object.assert_called_once_with(Bucket='testbucket', Key='test.txt')

def test_delete_bucket(mocker, minio_client):
    mock_delete_bucket = mocker.patch.object(minio_client.s3_client, 'delete_bucket')
    minio_client.delete_bucket('testbucket')
    mock_delete_bucket.assert_called_once_with(Bucket='testbucket')
