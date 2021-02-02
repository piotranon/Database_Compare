from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import datetime
import time
import csv
import json
from django.core.serializers.json import DjangoJSONEncoder

import pandas as pd

# clickhouse database driver
import clickhouse_driver
# postgres database driver
import psycopg2
# mssql database driver
import pymssql

from . import utils_DB


def clickhouse(request):
    clickhouse = ClickHouse()

    if request.method == 'GET':
        time1 = time.time_ns()
        data = clickhouse.executeQuery("Select * from Orders Limit 10")
        time2 = time.time_ns()
        return JsonResponse({"query": "Select * from Orders Limit 10", "data": json.loads(json.dumps(data, sort_keys=True, indent=1, cls=DjangoJSONEncoder)), "time": str(utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2))+" ms"}, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            if data.get('query') == "createTable":
                time1 = time.time_ns()
                clickhouse.createTable()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.createTable()+' ENGINE = MergeTree', "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "importData":
                time1 = time.time_ns()
                clickhouse.client.execute(
                    SQL.importData(), Data.generatorData())
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.importData(), "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "exportData":
                time1 = time.time_ns()
                clickhouse.exportData()
                time2 = time.time_ns()
                return JsonResponse({"query": "SELECT * FROM Orders", "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "dropTable":
                time1 = time.time_ns()
                clickhouse.dropTable()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.dropTable(), "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "countRecords":
                time1 = time.time_ns()
                amount = clickhouse.countRecords()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.countRecords(), "data": str(amount)+" Records", "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            else:
                print("custom SQl Query: "+str(data.get('query')))
                time1 = time.time_ns()
                amount = clickhouse.executeQuery(data.get('query'))
                time2 = time.time_ns()
                return JsonResponse({"query": data.get('query'), "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

        except Exception as e:

            return JsonResponse({"error": str(e)}, status=422)

        return HttpResponse(str(data))


def postgres(request):
    postgres = PostGres()

    if request.method == 'GET':
        postgres.executeQuery("Select * from Orders Limit 10")
        return HttpResponse("xdget")
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            if data.get('query') == "createTable":
                time1 = time.time_ns()
                postgres.createTable()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.createTable(), "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "importData":
                time1 = time.time_ns()
                postgres.importDataToTable()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.importData(), "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "exportData":
                time1 = time.time_ns()
                postgres.exportData()
                time2 = time.time_ns()
                return JsonResponse({"query": "COPY (SELECT * FROM Orders) TO STDOUT WITH CSV HEADER", "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "dropTable":
                time1 = time.time_ns()
                postgres.dropTable()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.dropTable(), "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            elif data.get('query') == "countRecords":
                time1 = time.time_ns()
                amount = postgres.countRecords()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.countRecords(), "data": str(amount)+" Records", "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

            else:
                print("custom SQl Query: "+str(data.get('query')))
                time1 = time.time_ns()
                amount = postgres.executeQuery(data.get('query'))
                time2 = time.time_ns()
                return JsonResponse({"query": data.get('query'), "time": utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2)}, status=200)

        except Exception as e:

            return JsonResponse({"error": str(e)}, status=422)

        return HttpResponse(str(data))


def mssql(request):
    mssql = MsSql()

    if request.method == 'GET':
        mssql.executeQuery("Select * from Orders Limit 10")
        return HttpResponse("xdget")
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            if data.get('query') == "createTable":
                time1 = time.time_ns()
                mssql.createTable()
                time2 = time.time_ns()
                return JsonResponse({"query": 'CREATE TABLE Orders ("Item Type" Varchar(250), "Order Date" Date, "Order ID" Int, "Units Sold" Float, "Unit Price" Float)', "time": str(utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2))}, status=200)

            elif data.get('query') == "importData":
                time1 = time.time_ns()
                mssql.importDataToTable()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.importData(), "time": str(utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2))}, status=200)

            elif data.get('query') == "exportData":
                time1 = time.time_ns()
                mssql.exportData()
                time2 = time.time_ns()
                return JsonResponse({"query": "SELECT * FROM Orders", "time": str(utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2))}, status=200)

            elif data.get('query') == "dropTable":
                time1 = time.time_ns()
                mssql.dropTable()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.dropTable(), "time": str(utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2))}, status=200)

            elif data.get('query') == "countRecords":
                time1 = time.time_ns()
                amount = mssql.countRecords()
                time2 = time.time_ns()
                return JsonResponse({"query": SQL.countRecords(), "data": str(amount)+" Records", "time": str(utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2))}, status=200)

            else:
                query = data.get('query')
                print("custom SQl Query: "+str(query))
                time1 = time.time_ns()
                data = mssql.executeQuery(query)
                time2 = time.time_ns()
                return JsonResponse({"query": query, "time": str(utils_DB.TimeDifferenceWithConversionToMiliseconds(time1, time2))}, status=200)

        except Exception as e:

            return JsonResponse({"error": str(e)}, status=422)

        return HttpResponse(str(data))


SQL = utils_DB.SQL()
Data = utils_DB.Data()


class ClickHouse:
    def disc(self):
        self.client.disconnect()

    def __init__(self):
        print("CLICKHOUSE CLIENT")
        self.client = clickhouse_driver.Client(
            'databasecompare_clickhouse-server_1')

    # create table structure
    def createTable(self):
        return self.client.execute(SQL.createTable()+' ENGINE = MergeTree')

    # insert data to database
    def importDataToTable(self):
        return self.client.execute(SQL.importData(), Data.generatorData())

    def exportData(self):
        data = self.client.execute("SELECT * FROM Orders")
        with open('exportClickhouse.csv', 'w') as f_output:
            exportFile = csv.writer(f_output)
            exportFile.writerows(data)
            f_output.close()
        return "exported"

    # drop table
    def dropTable(self):
        return self.client.execute(SQL.dropTable())

    # count amount of records
    def countRecords(self):
        return self.client.execute(SQL.countRecords())[0][0]

    def executeQuery(self, query):
        return self.client.execute(query)


class PostGres:
    def __init__(self):
        print("POSTGRES CLIENT")
        self.client = psycopg2.connect(
            "dbname='postgres' user='postgres' host='databasecompare_postgres_1' password='postgres'")
        self.cursor = self.client.cursor()

    # create table structure
    def createTable(self):
        data = self.cursor.execute(SQL.createTable())
        self.client.commit()
        return data

    # insert data to database
    def importDataToTable(self):
        with open('SalesRecords.csv', 'r') as f:
            next(f)  # Skip the header row.
            self.cursor.copy_from(f, 'Orders', sep=',')
            self.client.commit()
            return "inserted"

    # export data from database
    def exportData(self):
        SQL_for_file_output = "COPY (SELECT * FROM Orders) TO STDOUT WITH CSV HEADER"
        try:
            with open('exportPostgresSQL.csv', 'w') as f_output:
                self.cursor.copy_expert(SQL_for_file_output, f_output)
        except psycopg2.Error as e:
            print(e)

    # drop table
    def dropTable(self):
        data = self.cursor.execute(SQL.dropTable())
        self.client.commit()
        return data

    # count amount of records
    def countRecords(self):
        print("count_records")
        self.cursor.execute(SQL.countRecords())
        data = self.cursor.fetchone()[0]
        print("data")
        print(data)
        return data

    def executeQuery(self, query):
        data = self.cursor.execute(query)
        self.client.commit()
        return data


class MsSql:
    def disc(self):
        self.client.close()

    def __init__(self):
        print("Mssql")
        self.client = pymssql.connect(
            "databasecompare_mssql_1", "SA", "Pass@word", "master")
        self.cursor = self.client.cursor()

    # create table structure
    def createTable(self):
        data = self.cursor.execute(
            'CREATE TABLE Orders ("Item Type" Varchar(250), "Order Date" Date, "Order ID" Int, "Units Sold" Float, "Unit Price" Float)')
        self.client.commit()
        return data

    # insert data to database
    def importDataToTable(self):
        i = 0
        with open('SalesRecords.csv', 'r') as data:
            for line in csv.DictReader(data):
                if i % 100000 == 0:
                    print(str(i)+" rows inserted")
                    self.client.commit()
                i += 1
                self.cursor.execute(
                    "INSERT INTO Orders (\"Item Type\",\"Order Date\",\"Order ID\",\"Units Sold\",\"Unit Price\") VALUES (%(Item Type)s,%(Order Date)s,%(Order ID)d,%(Units Sold)d,%(Unit Price)d)", line)
        self.client.commit()

    # export data from database
    def exportData(self):
        self.cursor.execute("SELECT * FROM Orders")
        with open('exportMsSQL.csv', 'w') as f_output:
            exportFile = csv.writer(f_output)
            exportFile.writerow([i[0]
                                 for i in self.cursor.description])  # heading
            exportFile.writerows(self.cursor.fetchall())
            f_output.close()
            return "exported"

    # drop table
    def dropTable(self):
        data = self.cursor.execute(SQL.dropTable())
        self.client.commit()
        return data

    # count amount of records
    def countRecords(self):
        self.cursor.execute(SQL.countRecords())
        data = self.cursor.fetchone()[0]
        return data

    # execute sql query
    def executeQuery(self, query):
        data = self.cursor.execute(query)
        self.client.commit()
        return data
