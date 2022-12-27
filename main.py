import pymysql
import connectionInfo
import pandas as pd

# 기본 connect
# conn = pymysql.connect(
#     host=connectionInfo.HOST,
#     user=connectionInfo.USER,
#     password=connectionInfo.PSWD,
#     charset=connectionInfo.CHARSET
# )

# connection 생성
conn = connectionInfo.connections['conn1']

# 밑 처럼 해도 작동
# conn.select_db('data1')
# conn.select_db('data2')

# 커서 획득
cur = conn.cursor()


def __init__(cur):  # 초기화
    qry1 = "CREATE TABLE Movement (Acc INT, Gyro INT) IF NOT EXISTS Movement"
    qry2 = "CREATE TABLE Pulse (Pulse INT) IF NOT EXISTS Pulse"
    qry3 = "CREATE TABLE Breath (Breath INT) IF NOT EXISTS Breath"
    qry4 = "CREATE TABLE Temp (Temp INT) IF NOT EXISTS Temp"
    totalQry = """
        CREATE TABLE Movement (Acc INT, Gyro INT) IF NOT EXISTS Movement CREATE TABLE Pulse (Pulse INT) IF NOT EXISTS Pulse CREATE TABLE Breath (Breath INT) IF NOT EXISTS Breath CREATE TABLE Temp (Temp INT) IF NOT EXISTS Temp
    """
    cur.execute(totalQry)
    cur.execute(qry1)
    cur.execute(qry2)
    cur.execute(qry3)
    cur.execute(qry4)


def qry_select(cur, tableName):  # select data in field
    qry = "SELECT * FROM " + tableName
    cur.execute(qry)
    ret = cur.fetchall()
    print(ret)

# qry내에 table을 %s로 주면 실행 안됨.
# table이름을 qry내에 그냥 명시하거나 아래처럼 하면 실행 됨.


def qry_insert(cur, tableName, *args):  # insert data
    qry = "INSERT INTO " + tableName + " (Acc, Gyro) VALUES (%s,%s)"
    cur.execute(qry, args)
    ret = cur.fetchall()
    print(ret)


def qry_delete(cur, tableName, fieldName, data):  # delete field
    qry = "DELETE FROM " + tableName + " WHERE " + fieldName + "= %s"
    cur.execute(qry, (data))
    ret = cur.fetchall()
    print(ret)


def qry_drop(cur, databaseName, tableName):
    qry = None
    if databaseName is None:
        qry = "DROP TABLE IF EXISTS " + tableName
        cur.execute(qry)
    elif tableName is None:
        qry = "DROP DATABASE IF EXISTS " + databaseName
        cur.execute(qry)
    ret = cur.fetchall()
    print(ret)


def qry_table_check(cur, tableName):  # check Table
    qry = "SHOW TABLES LIKE %s"
    cur.execute(qry, (tableName))
    ret = cur.fetchall()
    print("TABLE EXSITS" if len(ret) == 1 else "NO TABLES")


# __init__(cur)
# qry_insert(cur, 'Movement', 3, 99)
# cur.execute("INSERT INTO Movement (Acc, Gyro) VALUES(3, 5)")
# qry_table_check(cur, "Body1")
# qry_select(cur, "move")
# qry_insert(cur, "move", 7, 7)
# cur.execute("INSERT INTO Move (Acc, Gyro) VALUES (7, 5)")

conn.commit()
conn.close()

