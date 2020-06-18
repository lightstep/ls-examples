'use strict';

const ACCESS_TOKEN = process.env.LS_ACCESS_TOKEN;
const SATELLITE_URL = process.env.LS_SATELLITE_URL || '127.0.0.1:55678';

const opentelemetry = require('@opentelemetry/api');
const { NodeTracerProvider } = require('@opentelemetry/node');
const { SimpleSpanProcessor } = require('@opentelemetry/tracing');
const { CollectorExporter } = require('@opentelemetry/exporter-collector');
const grpc = require('grpc');

const EXPORTER = process.env.EXPORTER || '';

module.exports = (serviceName) => {
    const provider = new NodeTracerProvider();

    const metadata = new grpc.Metadata();
    metadata.set('lightstep-access-token', ACCESS_TOKEN);
    const exporter = new CollectorExporter({
        serviceName: serviceName,
        url: SATELLITE_URL,
        credentials: grpc.credentials.createSsl(),
        metadata,
    });

    provider.addSpanProcessor(new SimpleSpanProcessor(exporter));

    // Initialize the OpenTelemetry APIs to use the NodeTracerProvider bindings
    provider.register();

    return opentelemetry.trace.getTracer('http-example');
};