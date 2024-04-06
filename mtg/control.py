# %%
import random
import time
from pathlib import Path

input_log = Path("C:\\Users\\loren\\Downloads\\UTC_Log - 03-17-2024 23.25.20.log")

with input_log.open("r") as f, open("foo.log", "w") as g:
    for line in f:
        g.write(line)
        time.sleep(random.randint(1, 3))
