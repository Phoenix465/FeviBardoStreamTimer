import time


with open("test.txt", "w") as f:
    for i in range(60):
        time.sleep(1)
        f.seek(0)
        f.write(f"{i}")
        f.truncate()