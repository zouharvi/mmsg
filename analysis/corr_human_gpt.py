#!/usr/bin/env python3

from utils import *
import numpy as np
import fig_utils
import os
from argparse import ArgumentParser

args = ArgumentParser()
args.add_argument("--model", "-m", default="gpt2_base")
args = args.parse_args()

data_gpt = collate_classes(load_logs_machine(model=args.model))
data_hum = collate_classes(load_logs())

ORDER = ['no_image', 'labels_text']


for config in ORDER:
    data_conf_hum = []
    data_conf_gpt = []
    # print(len(data_hum[config]["ratings"]), len(data_gpt[config]["ratings"]))
    for ratings_hum, sent_id in zip(data_hum[config]["ratings"], data_hum[config]["id"]):
        # print(sent_id)
        # this is slow but will fail if there's no match
        gpt_index = [i for i,x in enumerate(data_gpt[config]["id"]) if x == sent_id][0]

        # this will naturally flatten it
        data_conf_hum += ratings_hum
        data_conf_gpt += data_gpt[config]["ratings"][gpt_index]

    data_conf_hum_cnf = [x[0][1] for x in data_conf_hum]
    data_conf_hum_acc = [x[1][1] for x in data_conf_hum]
    data_conf_gpt_cnf = [x[0][1] for x in data_conf_gpt]
    data_conf_gpt_acc = [x[1][1] for x in data_conf_gpt]

    print("\nConfiguration", config)
    print(f"Correlation confidence: {np.corrcoef(data_conf_hum_cnf, data_conf_gpt_cnf)[0,1]:.2f}")
    print(f"Correlation accuracy:   {np.corrcoef(data_conf_hum_acc, data_conf_gpt_acc)[0,1]:.2f}")
