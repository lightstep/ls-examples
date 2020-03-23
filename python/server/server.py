#!/usr/bin/env python
import os
import random
import string

from ddtrace import tracer
from ddtrace.propagation.b3 import B3HTTPPropagator

tracer.configure(http_propagator=B3HTTPPropagator)
tracer.set_tags(
    {
        "lightstep.service_name": os.getenv("LIGHTSTEP_COMPONENT_NAME"),
        "service.version": os.getenv("LIGHTSTEP_SERVICE_VERSION"),
        "lightstep.access_token": os.getenv("SECRET_ACCESS_TOKEN"),
    }
)


from flask import Flask
app = Flask(__name__)


def _random_string(length):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(int(length)))

@app.route('/content/<length>')
def hello_world(length):
    return _random_string(length)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')