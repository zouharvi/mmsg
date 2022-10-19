#!/usr/bin/env bash

mkdir -p data

scp mmsg:multimodal-shannon-game/logs/*.jsonl data/v1/
rm -f data/v1/{harare_old,tuvalu,yemen}.jsonl
mv data/{v1,old}/zimbabwe.jsonl 