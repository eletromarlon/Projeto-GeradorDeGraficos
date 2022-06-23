import cx_Oracle
import psycopg
import sqlite3
import mysql.connector

#cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_3")

connection = None

def oracleConnection(username, password, dsn, query):
    saida = []
    connection = cx_Oracle.connect(username,password,dsn,encoding='UTF-8')
    cursor = connection.cursor()
    for row in cursor.execute(query):
        saida.append(row[0])
    connection.commit()
    connection.close()
    return saida

def mysqlConnection(host, dbname, user, password, consulta):
    connection = mysql.connector.connect(host=host, database=dbname, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute(consulta)
    column_names = [desc[0] for desc in cursor.description]
    return (cursor.fetchall(), column_names)
    connection.close()

def sqLiteConnection(consulta):
    connection = sqlite3.Connection("teste.db")
    cursor = connection.cursor()
    cursor.execute(consulta)
    column_names = [desc[0] for desc in cursor.description]
    return (cursor.fetchall(), column_names)
    # for row in cursor.execute(consulta):
    #     print(row)
    connection.close()

def postgresConnection(host, dbname, user, password, consulta):
    connection = psycopg.connect("host=" + host + " dbname=" + dbname + " user=" + user + " password=" + password)
    cursor = connection.cursor()
    cursor.execute(consulta)
    # for record in cursor:
    #     print(record)
    column_names = [desc[0] for desc in cursor.description]
    valor = cursor.fetchall()
    connection.commit()
    connection.close()
    return (valor,column_names)
    