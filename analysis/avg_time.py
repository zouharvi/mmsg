#!/usr/bin/env python3

from utils import *
import numpy as np

data = load_logs()

data_uid = defaultdict(list)

for line in data:
    data_uid[line["uid"]].append(line["time"])

print(len(data_uid))

times_all = []
for uid, uid_v in data_uid.items():
    uid = uid.replace("data/", "").replace(".jsonl", "")
    time_local = (max(uid_v)-min(uid_v))/1000/60
    print(f"{uid:<15}:", f"{time_local:.0f}m")
    times_all.append(time_local)
print(f"\navg:", f"{np.average(times_all):.0f}m")