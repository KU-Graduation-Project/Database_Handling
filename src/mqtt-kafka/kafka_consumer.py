import json
import multiprocessing
from asyncio.log import logger

import pymysql
from kafka import KafkaConsumer

import pandas as pd

from data_handle import DataHanlder as dh

"""user# 토픽에서 데이터 받아 db에 저장"""



class MessageConsumer:
    topic =""
    def __init__(self, topic):
        self.topic = topic
        self.data_set = {
            'time_stamp': [],
            'g_x': [],
            'g_y': [],
            'g_z': [],
            'a_x': [],
            'a_y': [],
            'a_z': [],
            'heartrate': [],
            'resp': [],
            'temp': [],
        }
        # DB연결
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='12341234', db='motionDB', charset='utf8')
        self.cur = self.conn.cursor()
        sql = 'DROP TABLE IF EXISTS ' + self.topic
        self.cur.execute(sql)

        print(self.topic + " table created")
        sql = 'CREATE TABLE ' + self.topic + ' (timestamp datetime PRIMARY KEY, ' \
                                             'g_x int(3), g_y int(3), g_z int(3), ' \
                                             'a_x int(3), a_y int(3), a_z int(3),' \
                                             'heartrate int(3), resp int(3), temp int(3))'
        self.cur.execute(sql)
        self.conn.commit()

        self.activate_listener()


    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 group_id='team',
                                 consumer_timeout_ms=60000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 #value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                                 )

        consumer.subscribe(self.topic)
        print(self.topic + ": consumer open")
        data_handler = dh(self.topic)
        try:
            for message in consumer:
                m_decode = str(message.value.decode("utf-8", "ignore"))
                m_in = m_decode[:len(m_decode)]

                m_json = json.loads(m_in)
                timestamp = m_json["timestamp"]
                g_x = str(m_json["g_x"])
                g_y = str(m_json["g_y"])
                g_z = str(m_json["g_z"])
                a_x = str(m_json["a_x"])
                a_y = str(m_json["a_y"])
                a_z = str(m_json["a_z"])
                heartrate = str(m_json["heartrate"])
                resp = str(m_json["resp"])
                temp = str(m_json["temp"])
                
                sql = 'INSERT INTO ' + self.topic + ' (timestamp, g_x, g_y, g_z, a_x, a_y, a_z, heartrate, resp, temp) VALUES (\''+timestamp+'\', '+g_x+', '+g_y+' ,'+g_z+' ,'+a_x+' ,'+a_y+', '+a_z+', '+heartrate+', '+resp+' ,'+temp+');'
                
                
                if self.cur.execute(sql):
                    print(self.topic + " DB save : " + str(m_json))
                # committing message manually after reading from the topic
                self.conn.commit()
                consumer.commit()
                
                # access to history db 
                data_handler.thread_data_handler(timestamp, g_x, g_y, g_z, a_x, a_y, a_z, heartrate, resp, temp)
                # dataFrame
                self.data_set['time_stamp'].append(timestamp)
                self.data_set['g_x'].append(g_x)
                self.data_set['g_y'].append(g_y)
                self.data_set['g_z'].append(g_z)
                self.data_set['a_x'].append(a_x)
                self.data_set['a_y'].append(a_y)
                self.data_set['a_z'].append(a_z)
                self.data_set['heartrate'].append(heartrate)
                self.data_set['resp'].append(resp)
                self.data_set['temp'].append(temp)
                
                
        except Exception as e:
            print(e)
            logger.exception("failed to create %s", e)
            
        finally:
            pd.DataFrame(self.data_set).to_csv(self.topic + '_sample.csv')
            consumer.close()


if __name__ == '__main__':
    user_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]
    
    pool = multiprocessing.Pool(processes=10)
    pool.map(MessageConsumer, user_list)
