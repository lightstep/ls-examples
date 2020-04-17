#
# example code to test ls-trace-py
#
# usage:
#   LIGHTSTEP_ACCESS_TOKEN=${SECRET_TOKEN} \
#   LIGHTSTEP_COMPONENT_NAME=demo-python \
#   LIGHTSTEP_SERVICE_VERSION=0.0.8 \
#   ls-trace-run python client.py

import os
import random
import requests
import time


if os.environ.get("OPENTELEMETRY_INSTRUMENTATION"):
    from urllib.parse import urlparse
    from opentelemetry import trace
    from opentelemetry.ext.lightstep import LightStepSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        ConsoleSpanExporter,
        BatchExportSpanProcessor,
    )

    o = urlparse(
        os.getenv("LS_METRICS_URL", "https://ingest.lightstep.com:443/metrics")
    )
    span_exporter = LightStepSpanExporter(
        os.getenv("LIGHTSTEP_SERVICE_NAME"),
        token=os.environ.get("LIGHTSTEP_ACCESS_TOKEN"),
        host=o.hostname,
    )

    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchExportSpanProcessor(span_exporter)
    )
else:
    from ddtrace import tracer
    from ddtrace.propagation.b3 import B3HTTPPropagator

    tracer.configure(http_propagator=B3HTTPPropagator)
    tracer.set_tags(
        {
            "lightstep.service_name": os.getenv("LIGHTSTEP_COMPONENT_NAME"),
            "service.version": os.getenv("LIGHTSTEP_SERVICE_VERSION"),
            "lightstep.access_token": os.getenv("LIGHTSTEP_ACCESS_TOKEN"),
        }
    )

if __name__ == "__main__":
    target = os.getenv("TARGET_URL", "http://localhost:8081")
    while True:
        url = f"{target}/content/{random.randint(1,1024)}"
        try:
            res = requests.get(url)
            print(f"Request to {url}, got {len(res.content)} bytes")
        except Exception as e:
            print(f"Request to {url} failed {e}")
            pass
        time.sleep(1)
