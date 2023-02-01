import threading
from multiprocessing.pool import ThreadPool
import pymysql

class DataHanlder:
    def __init__(self, thrd):
        self.buf = ["dummy", -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.thrd = thrd # 스레드 번호 t1, t2, ... 
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='12341234', db='historydb', charset='utf8')
        self.cur = self.conn.cursor()
        
        # self.thread_data_handler()
        
    def thread_data_handler(self, timestamp, g_x, g_y, g_z, a_x, a_y, a_z, heartrate, resp, temp):
        # user1, user2, ... , user10이 가지고 있는 데이터를 버퍼에 저장한다
        try:
            sql = 'INSERT INTO ' + self.thrd + ' (timestamp, g_x, g_y, g_z, a_x, a_y, a_z, heartrate, resp, temp) VALUES (\''+timestamp+'\', '+g_x+', '+g_y+' ,'+g_z+' ,'+a_x+' ,'+a_y+', '+a_z+', '+heartrate+', '+resp+' ,'+temp+');'
            if self.cur.execute(sql):
                print(self.thrd + " DB save!")
                self.conn.commit()
        except Exception as e:
            print("error ", e)
        
# def init_Thread(threads_list, threadnum = 10):
#     pool = ThreadPool(threadnum)
#     result = pool.map(DataHanlder, threads_list)
#     # print (result)
#     pool.close()
#     pool.join()
    
#     return result
# if __name__ == "__main__":
#     threads_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]
#     result = init_Thread(threads_list)