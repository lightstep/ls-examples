#!/usr/bin/env python
import os
import random
import string

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
    from opentelemetry.ext.flask import FlaskInstrumentor

    FlaskInstrumentor().instrument()

else:
    from ddtrace import tracer
    from ddtrace.constants import FILTERS_KEY
    from ddtrace.filters import FilterRequestsOnUrl
    from ddtrace.propagation.b3 import B3HTTPPropagator

    tracer.configure(http_propagator=B3HTTPPropagator, settings={})
    tracer.set_tags(
        {
            "lightstep.service_name": os.getenv("LIGHTSTEP_COMPONENT_NAME"),
            "service.version": os.getenv("LIGHTSTEP_SERVICE_VERSION"),
            "lightstep.access_token": os.getenv("LIGHTSTEP_ACCESS_TOKEN"),
        }
    )

from flask import Flask

app = Flask(__name__)


def _random_string(length):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(int(length)))


@app.route("/content/<length>")
def hello_world(length):
    return _random_string(length)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
