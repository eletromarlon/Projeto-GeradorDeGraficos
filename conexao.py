from multiprocessing import connection
import cx_Oracle

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

