#!/usr/bin/env bash

# run without buffer
nohup python3 -u ./server_logger/main.py >> logs/server.log &
