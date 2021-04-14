from project import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(userId):
    return User.query.get(userId)


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String, unique=True, index=True)
    passwordHash = db.Column(db.String(128))

    def __init__(self, mobile, password):
        self.mobile = mobile
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

    def __repr__(self):
        return f"User {self.mobile}"

class Portfolio(db.Model, UserMixin):

    __tablename__ = "portfolio"

    mobile = db.Column(db.String, db.ForeignKey('users.mobile'), primary_key=True)
    sticker = db .Column(db.String(10), nullable=False, primary_key=True)

    def __init__(self, mobile, sticker):
        self.mobile = mobile
        self.sticker = sticker

    def __repr__(self):
        return f"User {self.mobile} Stock {self.sticker}"
