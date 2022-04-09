#!/usr/bin/env python3

import json
import pickle
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import random


args = ArgumentParser()
args.add_argument("-d", "--dev", action="store_true")
args.add_argument("-s", "--seed", default=0, type=int)
args = args.parse_args()

random.seed(args.seed)

UID = [
    "harare", "lusaka", "sahara", "cardiff", "hanoi",
    "caracas", "montevideo", "washington", "kampala", "fanafuti"
]
UID_dev = [
    "zimbabwe", "zambia", "yemen", "wales", "venezuela",
    "vietnam", "vanuatu", "uzbekistan", "uruguay", "uganda", "tuvalu"
]
CONFIGS = [
    "labels_crop", "labels_all", "labels_text",
    "clear_all", "no_image", "original",
]

if args.dev:
    UID = UID_dev

with open(f"baked_queues/sents_length{'_dev' if args.dev else ''}.json", "r") as f:
    data = json.load(f)

os.makedirs("baked_queues/dev/", exist_ok=True)
os.makedirs("baked_queues/real/", exist_ok=True)

buckets = [set() for _ in data]

for uid in UID:
    queue = []
    for img_i, img in enumerate(data):
        config = random.sample(CONFIGS, k=1)[0]
        img_id_s = img["url"].split("/")[-1].rstrip(".jpg")
        queue.append({"id": img_id_s, "config": config})
        buckets[img_i].add(config)

    with open(f"baked_queues/{'dev/' if args.dev else 'real/'}{uid}.json", "w") as f:
        json.dump(queue, f, indent=4)

buckets = [len(x) for x in buckets]
print(sorted(buckets))