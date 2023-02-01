import random
import pymysql
import connectionInfo
import pandas as pd
import threading
import time
from queue import Queue, Empty, Full

# 기본 connect
# conn = pymysql.connect(
#     host=connectionInfo.HOST,
#     user=connectionInfo.USER,
#     password=connectionInfo.PSWD,
#     charset=connectionInfo.CHARSET
# )

# connection 생성
conn = connectionInfo.connections['conn1']
# conn2 = connectionInfo.connections['conn2']

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

send_queue = Queue()
send_queue2 = Queue()
client_key = -1
done = False
lock = threading.Lock()
dataSet = {
    'pulse': [],
}
dataSet2 = {
    'pulse': [],
}
exDf = None

def make_data_ex(t, datalist):
    # global send_queue
    global done
    # threading.Timer(time, make_data_ex, [1, datalist]).start()
    # x = [random.randint(0, 100) for _ in range(30)]
    # datalist.put(x)
    # save_data_ex(datalist)
    
    for _ in range(t):
        global client_key
        client_key = random.randint(1, 2)
        random_data = random.randint(0, 100)
        # lock.acquire()
        if client_key == 1:
            print("make_data to 1 ", random_data)
            send_queue.put(random_data)
        elif client_key == 2:
            print("make_data to 2 ", random_data)
            send_queue2.put(random_data)
        time.sleep(2)
        # lock.release()
    send_queue.join()
    send_queue2.join()
    done = True
    

def save_data_ex(datalist):
    # global send_queue
    global client_key
    while True:
        try:   
            # lock.acquire()
            get_data = None
            sql = ""
            if client_key == 1:
                conn = connectionInfo.connections['conn1']
                cur = conn.cursor();
                get_data = send_queue.get(timeout=2)
                print("save_data to 1 ", get_data)
                sql = "INSERT INTO tmp_table (temp) values (%s)"
                dataSet['pulse'].append(get_data)
                cur.execute(sql, get_data)
                send_queue.task_done()
            elif client_key == 2:
                conn = connectionInfo.connections['conn2']
                cur = conn.cursor();
                get_data = send_queue2.get(timeout=2)
                print("save_data to 2 ", get_data)
                sql = "INSERT INTO tmp_table (temp) values (%s)"
                dataSet2['pulse'].append(get_data)
                cur.execute(sql, get_data)
                send_queue2.task_done()            
            # sql = "INSERT INTO tmp_table (temp) values (%s)"
            # cur.executemany(sql, list(send_queue.queue))
            time.sleep(2)
            # lock.release()
            
        except Empty:
            # 문제 - 마지막 데이터까지 save 한 뒤, 종료까지 딜레이가 존재
            if done: 
                pd.DataFrame(dataSet).to_csv("sample1.csv")
                pd.DataFrame(dataSet2).to_csv("sample2.csv")
                conn.commit()
                conn.close()
                break
            else: continue

if __name__ == "__main__":
    threads = []
    t1 = threading.Thread(target=make_data_ex, args=(7, send_queue,))
    t1.start()
    threads.append(t1)

    t2 = threading.Thread(target=save_data_ex, args=(send_queue,))
    t2.start()
    threads.append(t2)
    
    for t in threads:
        t.join()