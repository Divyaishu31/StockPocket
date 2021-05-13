from project import db,application
from project.models import User, Portfolio
from flask import Flask,session,redirect,url_for
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin ,current_user

class MyModelViewP(ModelView):
     column_display_pk = True
     form_columns = ('id', 'mobile','sticker')

login = LoginManager(application)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class MyModelViewU(ModelView):
     column_display_pk = True
     form_columns = ('id', 'mobile','passwordHash')
     adminuser = User("Admin","adminpass")
     check_admin = User.query.filter(User.mobile == "Admin").first()
     if check_admin == None :
         db.session.add(adminuser)
         db.session.commit()

     def is_accessible(self):
         #print(current_user.get_id())
         return current_user.is_authenticated# and current_user.get_id()==1
         #is is_authenticated is the value that tells whether the current_user is logged in or not

     def inaccessible_callback(self,name,**kwargs):
         return redirect(url_for("users.login"))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

admina = Admin(application,index_view=MyAdminIndexView())
admina.add_view(MyModelViewP(Portfolio,db.session))
admina.add_view(MyModelViewU(User,db.session))

if __name__ == '__main__':
    application.run(debug=True, use_reloader=False)
