from project import db,application
from project.models import User, Portfolio
from flask import Flask,session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin ,current_user

# class MyModelViewP(ModelView):
#      column_display_pk = True
#      form_columns = ('id', 'mobile','sticker')

class MyModelViewU(ModelView):
     column_display_pk = True
     form_columns = ('id', 'mobile','passwordHash')

admina = Admin(application)
#admina.add_view(MyModelViewP(Portfolio,db.session))
admina.add_view(MyModelViewU(User,db.session))

if __name__ == '__main__':
    application.run(debug=True, use_reloader=False)
