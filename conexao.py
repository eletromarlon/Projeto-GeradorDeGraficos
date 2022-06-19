from multiprocessing import connection
import cx_Oracle
import psycopg
import sqlite3
import mysql.connector


#cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_3")

connection = None

def oracleConnection(username, password, dsn):
    saida = []
    connection = cx_Oracle.connect(username,password,dsn,encoding='UTF-8')
    cursor = connection.cursor()
    for row in cursor.execute("SELECT ID_PEDIDO FROM SIHPB_CIVIL.PEDIDO FETCH FIRST 100 ROWS ONLY"):
        saida.append(row[0])
    connection.commit()
    connection.close()
    return saida

def mysqlConnection(host, dbname, user, password, consulta):
    connection = mysql.connector.connect(host=host, database=dbname, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute(consulta)
    print(cursor.fetchall())
    connection.close()

def sqLiteConnection(consulta):
    connection = sqlite3.Connection("teste.db")
    cursor = connection.cursor()
    cursor.execute(consulta)
    print(cursor.fetchall())
    # for row in cursor.execute(consulta):
    #     print(row)
    connection.close()

def postgresConnection(host, dbname, user, password, consulta):
    connection = psycopg.connect("host=" + host + " dbname=" + dbname + " user=" + user + " password=" + password)
    cursor = connection.cursor()
    cursor.execute(consulta)
    # for record in cursor:
    #     print(record)
    print(cursor.fetchall())
    connection.commit()
    connection.close()

"""try:
    connection = cx_Oracle.connect(
        config.username,
        config.password,
        config.dsn,
        encoding=config.encoding)

    # show the version of the Oracle Database
    print(connection.version)
    cursor = connection.cursor
except cx_Oracle.Error as error:
    print(error)
finally:
    # release the connection
    if connection:
        connection.close()
"""

