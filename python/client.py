#!/usr/bin/env python
#
# example code to test ls-trace-py
#
# usage:
#   LS_ACCESS_TOKEN=${SECRET_TOKEN} \
#   LIGHTSTEP_COMPONENT_NAME=demo-python \
#   LIGHTSTEP_SERVICE_VERSION=0.0.8 \
#   ls-trace-run python client.py

from contextlib import contextmanager
import os
import random
import time

from common import get_tracer, start_span_operation

tracer = get_tracer()

import requests


def send_requests(target):
    integrations = ["pymongo", "redis", "sqlalchemy"]
    with start_span_operation(tracer)("client operation"):
        for i in integrations:
            url = f"{target}/{i}/{random.randint(1,1024)}"
            try:
                res = requests.get(url)
                print(f"Request to {url}, got {len(res.content)} bytes")
            except Exception as e:
                print(f"Request to {url} failed {e}")
                pass


if __name__ == "__main__":
    target = os.getenv("TARGET_URL", "http://localhost:8081")
    while True:
        send_requests(target)
        time.sleep(5)
