#!/usr/bin/env python3

import torch
import json
from PIL import Image, ImageDraw, ImageFont
import os
from argparse import ArgumentParser
from copy import deepcopy
from tqdm import tqdm

# labels
# model.names

args = ArgumentParser()
args.add_argument("-d", "--dev", action="store_true")
args = args.parse_args()

with open(f"baked_queues/sents_length{'_dev' if args.dev else ''}.json", "r") as f:
    data_control = json.load(f)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
results = model([img["url"] for img in data_control][:32])
data_detection = results.pandas().xyxy
results = results.tolist()

os.makedirs("img_data", exist_ok=True)
font = ImageFont.truetype('FreeMono.ttf', 16)

for i, (img, result) in tqdm(enumerate(zip(data_control, results))):
    str_id = img["url"].split("/")[-1]
    img_dir = "img_data/" + str_id.rstrip(".jpg") + "/"
    os.makedirs(img_dir, exist_ok=True)

    img_0 = Image.fromarray(result.imgs[0])
    # TODO: are all jpegs?
    img_0.save(img_dir + "original.jpg")

    result_la = deepcopy(result)
    result_la.display(labels=True, crop=False, save=False, render=True)
    result_la = Image.fromarray(result_la.imgs[0])
    result_la.save(img_dir + "labels_all.jpg")

    # result_ca = deepcopy(result)
    # result_ca.display(labels=False, crop=False, save=False, render=True)
    # result_ca = Image.fromarray(result_ca.imgs[0])
    # result_ca.save(img_dir + "clear_all.jpg")

    result_lc = deepcopy(result)
    result_lc = result_lc.display(
        labels=True, crop=True, save=False, render=True
    )
    # the x["im"] variable is broken (channel missing) so we crop manually

    # dict_keys(['box', 'conf', 'cls', 'label', 'im'])
    for i, crop in enumerate(result_lc):
        tmp = img_0.copy()
        tmp = tmp.crop((
            int(crop["box"][0]),
            int(crop["box"][1]) - 20,
            int(crop["box"][2]),
            int(crop["box"][3]),
        ))

        label_txt = crop["label"].split(" ")[0]
        min_width = font.getsize(label_txt)[0]+5
        scale = min_width/float(crop["box"][2]-crop["box"][0])

        tmp = tmp.resize((
            int(tmp.width * scale),
            int((tmp.height-20) * scale + 20),
        ))
        # tmp.save(img_dir + f"clear_crop_{i}.jpg")

        drawer = ImageDraw.Draw(tmp)
        drawer.rectangle(
            ((0, 0),
            (tmp.width, 17)),
            fill="black"
        )
        drawer.text((0,0), label_txt, fill="white", font=font)
        tmp.save(img_dir + f"labels_crop_{i}.jpg")

    with open(img_dir+"meta.json", "w") as f:
        f.write(json.dumps({
            "labels": [x["label"] for x in result_lc],
            "caption": img["caption"]
        }))