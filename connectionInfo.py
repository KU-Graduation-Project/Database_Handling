import pymysql
from pymysql.constants import CLIENT

HOST = '127.0.0.1'
USER = 'gradu'
PSWD = '12341234'
CHARSET = 'utf8'

# connection 객체
connections = {
    'conn1': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data1', charset=CHARSET) # client_flag=CLIENT.MULTI_STATEMENTS), # 클라이언트 1
    # 'conn2': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data2', charset=CHARSET), # 클라이언트 2
    # 'conn3': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data3', charset=CHARSET), # 클라이언트 3
    # 'conn4': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data4', charset=CHARSET), # 클라이언트 4
    # 'conn5': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data5', charset=CHARSET), # 클라이언트 5
    # 'conn6': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data6', charset=CHARSET), # 클라이언트 6
    # 'conn7': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data7', charset=CHARSET), # 클라이언트 7
    # 'conn8': pymysql.connect(host=HOST, user=USER, passwd=PSWD, database='data8', charset=CHARSET), # 클라이언트 8
}