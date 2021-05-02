import os
from twilio.rest import Client
#from fpdf import FPDF

import datetime

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def generate(quoteData):

    from project import db
    from project.models import User, Portfolio

    users = User.query.all() #List of User objects (strings) returned by __repr__ in class User

    for user in users:

        stocks = Portfolio.query.filter_by(mobile=str(user)).all()
        for i in range(len(stocks)):
            stocks[i] = str(stocks[i])

        # pdf = FPDF()
        # pdf.add_page()
        # pdf.set_font("Arial", size = 15)

        num = 1

        todaysDate = datetime.date.today()
        portfolioToday = "*" + "Markets on " + str(todaysDate) + "*\n\n"
        stockData = ""

        for stock in stocks:

            data = quoteData[stock]
            open = data["1. open"]
            close = data["4. close"]

            stockStick = str(num) + ". *" + stock + "*"
            stockData += stockStick + "\n"
            stockData += "Open: " + open + "\n" + "Close: " + close + "\n\n"

            # pdf.cell(200, 10, txt = str(num) + ". " + stock, ln = 1, align = 'C')
            # pdf.cell(200, 10, txt = stockData, ln = 2, align = 'C')

            num += 1

        #name = "Quotes - " + str(user) + " .pdf"
        # pdf.output(name)

        portfolioToday += stockData

        message = client.messages.create(
         body=portfolioToday,
         from_='whatsapp:+14155238886',
         to='whatsapp:' + str(user)
         )
