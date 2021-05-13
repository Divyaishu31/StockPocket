import requests
import json
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from project.services.generatePdf import generate

def queryStocks():
    from project import db
    from project.models import User, Portfolio

    apiKey = "X5422FZVMXL8U6SG"
    queryObj = Portfolio.query.with_entities(Portfolio.sticker).all() #List of Portfolio objects (strings) returned by
                                                                      #__repr__ in class Portfolio
    uniqueStocks = list(set([obj[0] for obj in queryObj]))
    print(uniqueStocks)
    quoteData = {}
    for i in range(len(uniqueStocks)):
        stock = uniqueStocks[i]
        print(stock)
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + stock + "&outputsize=compact&apikey=" + apiKey
        response = requests.request("GET", url)
        data = json.loads(response.text)
        quoteData[stock] = data["Time Series (Daily)"]["2021-04-08"]
        if i and ((i+1) % 5 == 0):
            time.sleep(65)
    generate(quoteData)

def helperThreadFunction():
    sched = BlockingScheduler()
    sched.add_job(queryStocks, 'cron', day_of_week='mon-sun', hour=17, minute=12, start_date='2021-04-10')
    sched.start()
