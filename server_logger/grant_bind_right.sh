#!/usr/bin/env bash

PATH_TO_PYTHON=$(readlink -f /usr/bin/python3)
echo "Grantink privileged port binding access to $PATH_TO_PYTHON"
sudo setcap CAP_NET_BIND_SERVICE=+eip $PATH_TO_PYTHON