#!/usr/bin/env python3

from utils import *
import numpy as np
import os

data = load_logs()

data_uid = defaultdict(list)

for line in data:
    data_uid[line["uid"]].append(line["time"])

print(len(data_uid))

for uid, uid_v in data_uid.items():
    uid = uid.replace("data/", "").replace(".jsonl", "")
    print(f"{uid:<15}:", f"{(max(uid_v)-min(uid_v))/1000/60:.0f}m")