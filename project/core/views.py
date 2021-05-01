from flask import render_template, request, Blueprint, url_for, flash, redirect
from project.users.forms import About
from urllib.request import urlopen
from bs4 import BeautifulSoup

core = Blueprint("core", __name__) #"core" (in parentheses) is the name of the blueprint

@core.route("/company", methods=["GET", "POST"])
def company():
    try:
        stck = request.args.get('stock')
        print(stck)

        url1 = "https://in.finance.yahoo.com/quote/" + stck + "/profile"
        url2 = "https://in.finance.yahoo.com/quote/" + stck

        page = urlopen(url1)
        page1 = urlopen(url2)


        soup = BeautifulSoup(page,'html.parser')
        soup1 = BeautifulSoup(page1,'html.parser')



        company_name = soup.find_all("h1", {"class": "D(ib) Fz(18px)"})[0].string

        i1 = soup.find_all("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].string

        #i2 = soup.find_all("span", {"class": "Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor"})[0].string


        description=soup.find_all("p",{"class": "Mt(15px) Lh(1.6)"})[0].string



        table = soup1.find_all("table", {"class": "W(100%)"})
        l=[]
        for tr in table:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            l.append(row)
        tag=[]
        value=[]
        for i in range(len(l[0])):
            if (i%2==0):
                tag.append(l[0][i])
            else:
                value.append(l[0][i])

        for i in range(len(l[1])):
            if (i%2==0):
                tag.append(l[1][i])
            else:
                value.append(l[1][i])


        return render_template("company.html",company_name=company_name,i1=i1,description=description,tv=zip(tag,value))
    except Exception as e:
        return render_template("errorPages/404.html")

@core.route("/",methods=["GET", "POST"])
def index():

    form = About()

    if form.validate_on_submit():
        stock = form.tag.data



        return redirect(url_for("core.company",stock = stock))
    return render_template("search.html",form = form)


@core.route("/info")
def info():
    return render_template("info.html")
