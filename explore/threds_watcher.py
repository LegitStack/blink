from threading import Thread
import time


a = 0  # global variable


def thread1(threadname):
    global a
    b = a
    print(f'a {a}, b {b}')
    for k in range(50):
        print(f'a {a}, b {b}')
        if b != a:
            print(f'changed a {a}, b {b}')
        b = a
        time.sleep(0.1)


thread1 = Thread(target=thread1, args=("Thread-1",))

try:
    thread1.start()
except (KeyboardInterrupt, SystemExit):
    cleanup_stop_thread()
    sys.exit()

# join blocks all other behavior until threads have finished:
# thread1.join()

for k in range(50):
    a += 1
    time.sleep(0.2)
    if k == 5:
        a += 100
