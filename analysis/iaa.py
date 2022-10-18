#!/usr/bin/env python3

from utils import *
import numpy as np
import os

data = load_logs()

data_sid = defaultdict(list)

for line in data:
    data_sid[line["id"]].append([word[0][1] for word in line["ratings"]])

for sid, sid_v in data_sid.items():
    if len(sid_v) == 1:
        continue

    for uid_v in sid_v:
        print(uid_v)

    print("="*15)
    continue
    mid = min([len(l) for l in sid_v])
    sid_v = [l[:int(mid)] for l in sid_v]
    a = np.average(np.array(sid_v), axis=0)
    print(a.shape, a)
