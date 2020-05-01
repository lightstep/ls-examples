#!/usr/bin/env python
import os
import random
import string

import redis
from pymongo import MongoClient
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if os.environ.get("OPENTELEMETRY_INSTRUMENTATION"):
    if os.environ.get("OPENTELEMETRY_EXPORTER") == "collector":
        from opentelemetry.ext.otcollector.trace_exporter import CollectorSpanExporter
        from opentelemetry.ext.otcollector.metrics_exporter import (
            CollectorMetricsExporter,
        )

        span_exporter = CollectorSpanExporter(
            service_name=os.getenv("LIGHTSTEP_SERVICE_NAME"),
            endpoint=os.getenv("COLLECTOR_ENDPOINT", "localhost:55678"),
        )
    else:
        from urllib.parse import urlparse
        from opentelemetry.ext.lightstep import LightStepSpanExporter

        o = urlparse(
            os.getenv("LS_METRICS_URL", "https://ingest.lightstep.com:443/metrics")
        )
        span_exporter = LightStepSpanExporter(
            os.getenv("LIGHTSTEP_SERVICE_NAME"),
            token=os.environ.get("LIGHTSTEP_ACCESS_TOKEN"),
            host=o.hostname,
            service_version=os.getenv("LIGHTSTEP_SERVICE_VERSION"),
        )

    from opentelemetry import trace
    from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

    trace.get_tracer_provider().add_span_processor(
        BatchExportSpanProcessor(span_exporter)
    )

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

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = "address"
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship(Person)


def _random_string(length):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(int(length)))


@app.route("/redis/<length>")
def redis_integration(length):
    r = redis.Redis(host="redis", port=6379)
    r.mset({"length": _random_string(length)})
    return str(r.get("length"))


@app.route("/pymongo/<length>")
def pymongo_integration(length):
    client = MongoClient("mongo", 27017, serverSelectionTimeoutMS=2000)
    db = client["opentelemetry-tests"]
    collection = db["tests"]
    collection.find_one()
    return _random_string(length)


@app.route("/sqlalchemy/<length>")
def sqlalchemy_integration(length):
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine("sqlite:///sqlalchemy_example.db")

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    return str(_random_string(length))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
