import time
import datetime
from csv import DictReader


def TimeDifferenceWithConversionToMiliseconds(time, time1):
    msTime = round((time1-time)/1e6, 2)
    secTime = round((time1-time)/1e9, 2)
    minTime = round(((time1-time)/1e9)/60, 2)
    sec = ""

    if (msTime >= 1000):
        sec = "<br/>"+str(secTime)+" sec"
    min = ""
    if (secTime >= 60):
        min = "<br/>"+str(minTime) + " min"
    return str(msTime)+" ms"+sec+min


class SQL:
    def createTable(self):
        #  Int32
        return 'CREATE TABLE IF NOT EXISTS Orders ("Item Type" Varchar(250), "Order Date" Date, "Order ID" Int, "Units Sold" Float, "Unit Price" Float, PRIMARY KEY ("Order ID"))'

    def importData(self):
        return 'INSERT INTO Orders ("Item Type", "Order Date", "Order ID", "Units Sold", "Unit Price") VALUES'

    def dropTable(self):
        return 'DROP TABLE Orders'

    def countRecords(self):
        return 'SELECT count(*) FROM Orders'


class Data:
    def generatorData(self):
        return iter_csv('SalesRecords.csv')


def convertToDate(date):
    return datetime.datetime.strptime(date, "%m/%d/%Y").date()


def iter_csv(filename):
    converters = {
        'Order ID': int,
        'Order Date': convertToDate,
        'Ship Date': convertToDate,
        'Units Sold': float,
        'Unit Price': float,
    }
    with open(filename, 'r') as f:
        print('file start')
        reader = DictReader(f)
        for line in reader:
            yield {k: (converters[k](v) if k in converters else v) for k, v in line.items()}
        print('file end')
