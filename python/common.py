import os


def start_span_operation(tracer):
    if os.environ.get("OPENTELEMETRY_INSTRUMENTATION"):
        return tracer.start_as_current_span
    else:
        from ddtrace import tracer

        return tracer.trace


def get_otlp_exporter():
    import grpc
    from opentelemetry.ext.otlp.trace_exporter import OTLPSpanExporter

    if os.getenv("INSECURE", False):
        credentials = None
    else:
        credentials = grpc.ssl_channel_credentials()

    return OTLPSpanExporter(
        credentials=credentials,
        endpoint=os.getenv("COLLECTOR_ENDPOINT", "localhost:55680"),
        metadata=(("lightstep-access-token", os.environ.get("LS_ACCESS_TOKEN")),),
    )


def get_ls_exporter():
    from urllib.parse import urlparse
    from opentelemetry.ext.lightstep import LightStepSpanExporter

    o = urlparse(
        os.getenv("LS_METRICS_URL", "https://ingest.lightstep.com:443/metrics")
    )
    return LightStepSpanExporter(
        os.getenv("LIGHTSTEP_SERVICE_NAME"),
        token=os.environ.get("LS_ACCESS_TOKEN"),
        host=o.hostname,
        service_version=os.getenv("LIGHTSTEP_SERVICE_VERSION"),
    )


def get_otel_tracer():
    if os.environ.get("OPENTELEMETRY_EXPORTER") == "collector":
        span_exporter = get_otlp_exporter()
    else:
        span_exporter = get_ls_exporter()

    from opentelemetry import trace
    from opentelemetry.sdk.trace import Resource
    from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

    trace.get_tracer_provider().add_span_processor(
        BatchExportSpanProcessor(span_exporter)
    )
    trace.get_tracer_provider().resource = Resource(
        {
            "service.name": os.getenv("LIGHTSTEP_SERVICE_NAME"),
            "service.version": os.getenv("LIGHTSTEP_SERVICE_VERSION"),
        }
    )
    return trace.get_tracer(__name__)


def get_ls_tracer():
    from ddtrace import tracer
    from ddtrace.constants import FILTERS_KEY
    from ddtrace.filters import FilterRequestsOnUrl
    from ddtrace.propagation.b3 import B3HTTPPropagator

    tracer.configure(http_propagator=B3HTTPPropagator, settings={})
    tracer.set_tags(
        {
            "lightstep.service_name": os.getenv("LIGHTSTEP_COMPONENT_NAME"),
            "service.version": os.getenv("LIGHTSTEP_SERVICE_VERSION"),
            "lightstep.access_token": os.getenv("LS_ACCESS_TOKEN"),
        }
    )


def get_tracer():
    if os.environ.get("OPENTELEMETRY_INSTRUMENTATION"):
        return get_otel_tracer()
    return get_ls_tracer()
