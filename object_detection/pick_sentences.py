#!/usr/bin/env python3

import json
from collections import Counter, defaultdict
from argparse import ArgumentParser
import random

args = ArgumentParser()
args.add_argument("-d", "--dev", action="store_true")
args = args.parse_args()

data_control = []
lengths = Counter()

buckets_to_fulfill = defaultdict(lambda: 0) | {
    8: 2,
    9: 2,
    10: 2,
    11: 2,
    12: 2,
    13: 2,
    14: 2,
    15: 2,
}
used_imgs = set()
ANN_BAN = {407404, 22951, 601937, 164522, 610124, 733653, 825720, 706927}
IMG_BAN = {}
buckets = []

with open("captions_val2017.json", "r") as f:
    data_coco = json.load(f)

random.seed(0)
random.shuffle(data_coco["images"])

print("Total count:", len(data_coco["images"]))

def filter_ann(ann):
    if ann["caption"].isupper():
        return False
    if "  " in ann["caption"]:
        return False
    if not ann["caption"][0].isupper() or not ann["caption"][0].isalpha():
        return False
    if ann["id"] in ANN_BAN:
        return False
    if "toilet" in ann["caption"]:
        return False
    if ann["caption"].count(".") != 1:
        return False
    return True

for img_i, img in enumerate(data_coco["images"][(250 if args.dev else 0):]):
    # this is an inefficient but quick way to match annotations
    # ann["caption"] and ann["id"]
    captions = [{
            "url": img["coco_url"],
            "ann_id": ann["id"],
            "img_id": ann["image_id"],
            "caption": ann["caption"].strip(),
            "length": len(ann["caption"].split()),
        }
        for ann in data_coco["annotations"]
        if img["id"] == ann["image_id"] and ann["image_id"] not in IMG_BAN and filter_ann(ann)
    ]

    lengths.update([ann["length"] for ann in captions])

    for ann in captions:
        if (buckets_to_fulfill[ann["length"]] > 0) and (ann["img_id"] not in used_imgs):
            used_imgs.add(ann["img_id"])
            buckets.append(ann)
            buckets_to_fulfill[ann["length"]] -= 1
            print("img_i:", img_i)
            break
    
    if sum(buckets_to_fulfill.values()) == 0:
        break


print(lengths)
# plt.scatter(lengths.keys(), lengths.values())
# plt.show()

with open(f"baked_queues/sents_length{'_dev' if args.dev else ''}.json", "w") as f:
    json.dump(buckets, f, indent=4)