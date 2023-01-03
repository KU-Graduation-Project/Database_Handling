import threading

# Thread 공부용 임시 파일
def plus(num):
    global number
    for i in range(num):
        lock.acquire()
        number += 1
        print(number)
        lock.release()
    print('thread 1 exit...')
    
def minus(num):
    global number
    for i in range(num):
        lock.acquire()
        number -= 1
        print(number)
        lock.release()
    print('thread2 exit...')
    
number = 0
lock = threading.Lock()
t1 = threading.Thread(target=plus, args=(10,))
t2 = threading.Thread(target=minus, args=(10,))

t1.start()
t2.start()

t1.join()
t2.join()

print('main exit..')