from project.models import User, Portfolio
from project import application, db
from project.models import User, Portfolio


def test_new_user(new_user):#mention the fixture name that it is using
    """
    GIVEN a User model
    WHEN a new User is created
    THEN mobile,passwordHash are defined correctly or not
    """
    assert new_user.mobile == '123456789'
    assert new_user.passwordHash != 'spepassword'

def test_portfolio(portfolio):
    """
    GIVEN a Portfolio model
    WHEN a new record is accessed
    THEN mobile,sticker are checked whether correct or not
    """
    assert portfolio.mobile == '123456789'
    assert portfolio.sticker == 'AMZN'

def test_project():
    response = application.test_client().get('/')
    assert response.status_code == 200
