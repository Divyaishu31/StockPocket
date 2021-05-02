from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db
from project.models import User, Portfolio
from project.users.forms import RegistrationForm, LoginForm, AddStockForm,UpdateForm,About, Compare
#from admin import MyModelViewP
from admin import MyModelViewU
import os
from twilio.rest import Client
from urllib.request import urlopen
from bs4 import BeautifulSoup

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
        check_stock = Portfolio.query.filter(Portfolio.mobile == str(stock.mobile),Portfolio.sticker == str(stock.sticker)).first()
        if check_stock == None :
            db.session.add(stock)
            db.session.commit()
        return redirect(url_for("users.addStock"))
    return render_template("addStock.html",form=form)

@users.route('/show',methods = ['GET','POST'])
@login_required
def show():
     stickers = Portfolio.query.filter_by(mobile = current_user.mobile).all() #List
     for i in range(len(stickers)):
         stickers[i] = str(stickers[i])
     return render_template('showpocket.html',stickers=stickers)

@users.route('/update',methods = ['GET','POST'])
@login_required
def update():
    stock = Portfolio.query.filter_by(mobile=current_user.mobile)
    form = UpdateForm()
    if form.validate_on_submit():
        sticker = form.sticker.data
        stock = Portfolio.query.filter_by(mobile=current_user.mobile,sticker=sticker).first()
        if stock is not None:
            db.session.delete(stock)
            db.session.commit()
        return redirect(url_for("users.show"))
    return render_template("update.html",form=form)

@users.route("/compare", methods=["GET", "POST"])
def compare():
    try:
        stck1 = request.args.get('stock1')
        stck2 = request.args.get('stock2')
        url1 = "https://in.finance.yahoo.com/quote/" + stck1
        url2 = "https://in.finance.yahoo.com/quote/" + stck2
        page1 = urlopen(url1)
        page2=urlopen(url2)
        soup1 = BeautifulSoup(page1,'html.parser')
        soup2 = BeautifulSoup(page2,'html.parser')
        company_name1 = soup1.find_all("h1", {"class": "D(ib) Fz(18px)"})[0].string
        i11 = soup1.find_all("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].string
        table1 = soup1.find_all("table", {"class": "W(100%)"})
        l1=[]
        for tr in table1:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            l1.append(row)
        tag1=[]
        value1=[]
        for i in range(len(l1[0])):
            if (i%2==0):
                tag1.append(l1[0][i])
            else:
                value1.append(l1[0][i])

        for i in range(len(l1[1])):
            if (i%2==0):
                tag1.append(l1[1][i])
            else:
                value1.append(l1[1][i])

        company_name2 = soup2.find_all("h1", {"class": "D(ib) Fz(18px)"})[0].string
        i12 = soup2.find_all("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].string
        table2 = soup2.find_all("table", {"class": "W(100%)"})
        l2=[]
        for tr in table2:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            l2.append(row)
        tag2=[]
        value2=[]
        for i in range(len(l2[0])):
            if (i%2==0):
                tag2.append(l2[0][i])
            else:
                value2.append(l2[0][i])

        for i in range(len(l2[1])):
            if (i%2==0):
                tag2.append(l2[1][i])
            else:
                value2.append(l2[1][i])
                return render_template("compare.html",company_name1=company_name1,i11=i11,company_name2=company_name2,i12=i12,tv=zip(tag1,value1,value2))
    except Exception as e:
        return render_template("errorPages/404.html")

@users.route("/sercom", methods=["GET", "POST"])
def sercom():
    form = Compare()
    if form.validate_on_submit():
        stock1 = form.comp1.data
        stock2 = form.comp2.data
        return redirect(url_for("users.compare",stock1 = stock1,stock2 = stock2))
    return render_template("compsearch.html",form = form)
