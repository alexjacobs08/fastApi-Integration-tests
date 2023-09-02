import pytest

import boto3
from moto import mock_s3
from mongomock import MongoClient

from fastapi.testclient import TestClient

from app.auth import get_auth
from app.models import TokenData

bucket = 'fastAPI-example-app-user-preferences-store'


class MockMongoClient:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        return self.db

    def __exit__(self, *args):
        pass


@pytest.fixture
def mock_mongodb():
    def mock_get_mongodb():
        mock_client = MongoClient()
        return MockMongoClient(mock_client.db)

    return mock_get_mongodb


@pytest.fixture
def mock_mongodb_initialized():
    def mock_get_mongodb():
        mock_client = MongoClient()
        mock_client.db.preferences.insert_one({"username": "alexjacobs", "city": "Berlin"})
        return MockMongoClient(mock_client.db)

    return mock_get_mongodb


@pytest.fixture(scope="session")
def mock_s3_bucket():
    with mock_s3():
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=bucket)
        # s3_client = boto3.client('s3', region_name='us-east-1')
        # s3_client.upload_file('tests/assets/duck.png', bucket, 'profile_pics/alexjacobs.png') we could upload a test file here
        yield


@pytest.fixture
def client(mock_s3_bucket):
    # we patch auth within our client fixture
    from app.main import app

    def mock_get_auth():
        return TokenData(username="alexjacobs")

    app.dependency_overrides[get_auth] = mock_get_auth
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_unpatched_auth():
    # we don't patch auth for this client
    from app.main import app

    with TestClient(app) as test_client_2:
        yield test_client_2


@pytest.fixture
def mock_get_auth_factory():
    def mock_get_auth():
        return TokenData(username="alexjacobs")

    return mock_get_auth
