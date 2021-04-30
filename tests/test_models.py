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











# def test_empty_db(client):
#     """Start with a blank database."""
#
#     rv = client.get('/')
#     assert b'No entries here so far' in rv.data
#
# import unittest
# from project import application
# BasicTestCase(unittest.TestCase):
#     def test_home(self):
#         tester = app.test_client(self)
#         response = tester.get('/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data, b'Hello World!')def test_other(self):
#         tester = app.test_client(self)
#         response = tester.get('a', content_type='html/text')
#         self.assertEqual(response.status_code, 404)
#         self.assertTrue(b'does not exist' in response.data)if __name__ == '__main__':
#     unittest.main()

def test_application(client):
    pass
    #assert not client.application.debug
