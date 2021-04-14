from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db
from project.models import User, Portfolio
from project.users.forms import RegistrationForm, LoginForm, AddStockForm

import os
from twilio.rest import Client

users = Blueprint("users", __name__)

@users.route("/Sign up", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(mobile=form.mobile.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                                      body='Hi there! Thanks for registering!!',
                                      from_='whatsapp:+14155238886',
                                      to='whatsapp:' + form.mobile.data
                                  )

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(mobile=form.mobile.data).first()

        if user is not None and user.checkPassword(form.password.data):

            login_user(user)

            #For the case where user was earlier trying to visit a page that requires login
            next = request.args.get("next")

            if next == None or not next[0] == "/":
                next = url_for("core.index")

            return redirect(next)

    return render_template("login.html",form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route("/addStock", methods=["GET", "POST"])
@login_required
def addStock():

    form = AddStockForm()

    if form.validate_on_submit():

        stock = Portfolio(mobile=current_user.mobile, sticker=form.sticker.data)

        db.session.add(stock)
        db.session.commit()

        # Puppy.query.filter_by(name="Frankie")

        stock = Portfolio.query.filter_by(mobile=current_user.mobile)
        print(stock.all())

        return redirect(url_for("users.addStock"))

    return render_template("addStock.html",form=form)
