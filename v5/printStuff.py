import time

for i in range(10):
    print(f"\rLoading... {i}", end="", flush=True)
    time.sleep(0.5)  # Simulate some processing