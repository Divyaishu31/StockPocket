import pytest
from project.models import User, Portfolio


@pytest.fixture(scope='module')
def new_user():
    user = User('123456789', 'spepassword')
    return user

@pytest.fixture(scope='module')
def portfolio():
    record = Portfolio('123456789', 'AMZN')
    return record

##trying to create the client() named setup of the flask application which will be used for testing
# from flask import Flask
# from flask.testing import FlaskClient
#
# @pytest.fixture
# def client():
#
#     application = Flask(__name__)
#     application.config["SECRET_KEY"] = "mysecret"
#     with application.test_client() as client:
#             yield application
