import json
from collections import defaultdict
import numpy as np
from glob import glob


def time_filter(v, med, cap=15):
    if v > cap:
        return med
    return v


def process_time(ratings):
    ratings = [
        [[x[0][0] / 1000, x[0][1]], [x[1][0] / 1000, x[1][1]]]
        for x in ratings
    ]
    median_conf = np.median([x[0][0] for x in ratings])
    median_eval = np.median([x[1][0] for x in ratings])

    ratings = [
        [
            [time_filter(x[0][0], med=median_conf), x[0][1]],
            [time_filter(x[1][0], med=median_eval), x[1][1]]
        ]
        for x in ratings
    ]
    return ratings


def load_logs(uids=None):
    if uids is None:
        uids = glob("data/*.jsonl")
    else:
        uids = [f"data/{uid}.jsonl" for uid in uids]
    

    data = []
    for uid in uids:
        # hard remove tuvaul and yemen
        if "tuvalu" in uid or "yemen" in uid:
            continue

        with open(f"{uid}", "r") as f:
            data_local = [{
                "uid": uid,
                **json.loads(line)
            }
                for line in f.readlines()
            ]
            data_local = [{
                **v,
                "ratings": process_time(v["ratings"])
            } for v in data_local]
            data += data_local
    return data


def collate_classes(data):
    data_c = defaultdict(lambda: defaultdict(list))

    # first level
    for line in data:
        for key in {"config", "sent", "id", "ratings"}:
            data_c[line["config"]][key].append(line[key])

    return dict(data_c)
