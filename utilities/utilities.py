import time

def waitFor(interval):
    start_time = time.time()
    while time.time() - start_time <= interval:
        print("Measurement in process...")
        time.sleep(2)
