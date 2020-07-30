#!/bin/bash

export LS_SERVICE_NAME="java-server"
export LS_SERVICE_VERSION="0.0.1"
export LS_ACCESS_TOKEN=""

#export OTEL_EXPORTER_OTLP_SPAN_ENDPOINT="staging.ingest.lightstep.com"
#export OTEL_EXPORTER_OTLP_SPAN_INSECURE="true"
#export OTEL_PROPAGATORS="tracecontext"
#export OTEL_LOG_LEVEL=""
#export OTEL_RESOURCE_LABELS="host=here.com,deployment=99"

java -javaagent:lightstep-opentelemetry-javaagent-0.1.0-SNAPSHOT.jar \
	-jar target/server.jar
