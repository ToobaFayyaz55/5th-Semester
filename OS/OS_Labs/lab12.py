# producer_consumer.py
import threading
import time
import random
from collections import deque
BUFFER_SIZE = 5
PRODUCER_COUNT = 2
CONSUMER_COUNT = 3

buffer = deque(maxlen=BUFFER_SIZE)
empty = threading.Semaphore(BUFFER_SIZE)  # Tracks empty slots
full = threading.Semaphore(0)             # Tracks filled slots
mutex = threading.Lock()                   # Ensures mutual exclusion

def producer(producer_id):
    global buffer
    item_counter = 0
    while True:
        item = f"Item-{producer_id}-{item_counter}"
        empty.acquire()
        mutex.acquire()
        buffer.append(item)
        print(f"Producer {producer_id} produced {item}. Buffer: {list(buffer)}")
        mutex.release()
        full.release()
        item_counter += 1
        time.sleep(random.uniform(0.5, 2))

# --- Consumer Thread ---
def consumer(consumer_id):
    global buffer
    while True:
        full.acquire()
        mutex.acquire()
        item = buffer.popleft()
        print(f"Consumer {consumer_id} consumed {item}. Buffer: {list(buffer)}")
        mutex.release()
        empty.release()
        time.sleep(random.uniform(1, 3))

# --- Main Application ---
if __name__ == "__main__":
    threads = []
    for i in range(PRODUCER_COUNT):
        thread = threading.Thread(target=producer, args=(i,))
        threads.append(thread)
        thread.start()
    for i in range(CONSUMER_COUNT):
        thread = threading.Thread(target=consumer, args=(i,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
