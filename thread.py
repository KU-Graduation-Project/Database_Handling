# Thread 공부용 임시 파일
import threading

number = 0
lock = threading.Lock()

def plus(num):
    global number
    print("number = ", end=""), print(num)
    lock.acquire()
    for _ in range(num):
        number += 1
    lock.release()
    print('thread1 exit...')
    
def plus2(num):
    global number
    print("number = ", end=""), print(num)
    lock.acquire()
    for _ in range(num):        
        number += 1
    lock.release()
    print('thread2 exit...')
    
t1 = threading.Thread(target=plus, args=(50000000,))
t2 = threading.Thread(target=plus2, args=(50000000,))

t1.start()
t2.start()

t1.join()
t2.join()

print(number)
print('main exit..')