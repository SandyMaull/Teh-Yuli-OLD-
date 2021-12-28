import mysql.connector
from ext.db_module import connection
import json


def one(table, field, value):
    db = connection.connect()
    cursor = db.cursor()
    sql = "SELECT * FROM {table} WHERE {field} = '{value}'".format(table = table, field = field, value = value)
    try:
        cursor.execute(sql)
        data = cursor.description
        result = cursor.fetchone()
        i = 0
        column_name = {}
        while i < len(data):
            column_name[data[i][0]] = str(result[i])
            i += 1
        return json.dumps(column_name)
    except:
        print('Error when fetching data!')
        return False

def many(table, field, value):
    db = connection.connect()
    cursor = db.cursor()
    sql = "SELECT * FROM {table} WHERE {field} = '{value}'".format(table = table, field = field, value = value)
    try:
        cursor.execute(sql)
        data = cursor.description
        result = cursor.fetchall()
        g = 0
        finaldata = {}
        for items in result:
            column_name = {}
            i = 0
            while i < len(data):
                column_name[data[i][0]] = str(items[i])
                i += 1
            finaldata[g] = column_name
            g += 1
        return json.dumps(finaldata)
    except:
        print('Error when fetching data!')
        return False

def all(table):
    db = connection.connect()
    cursor = db.cursor()
    sql = "SELECT * FROM {table}".format(table = table)
    try:
        cursor.execute(sql)
        data = cursor.description
        result = cursor.fetchall()
        g = 0
        finaldata = {}
        for items in result:
            column_name = {}
            i = 0
            while i < len(data):
                column_name[data[i][0]] = str(items[i])
                i += 1
            finaldata[g] = column_name
            g += 1
        return json.dumps(finaldata)
    except:
        print('Error when fetching data!')
        return False