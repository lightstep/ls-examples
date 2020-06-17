'use strict';

const ACCESS_TOKEN = process.env.LIGHTSTEP_ACCESS_TOKEN;
const COMPONENT_NAME =
    process.env.LIGHTSTEP_COMPONENT_NAME || 'ls-trace-js-client';
const SERVICE_VERSION = process.env.LIGHTSTEP_SERVICE_VERSION || '0.0.1';
const TARGET_URL = process.env.TARGET_URL || 'http://localhost:8080/ping';

const tracer = require('./tracer')('example-http-client');
// eslint-disable-next-line import/order
const http = require('http');

/** A function which makes requests and handles response. */
function makeRequest() {
    // span corresponds to outgoing requests. Here, we have manually created
    // the span, which is created to track work that happens outside of the
    // request lifecycle entirely.
    const span = tracer.startSpan('makeRequest');
    tracer.withSpan(span, () => {
        http.get(TARGET_URL, resp => {
            let data = '';
            resp.on('data', chunk => (data += chunk));
            resp.on('end', () => console.log(`recv: ${data}`));
            resp.on('error', err => console.log('Error: ' + err.message));
        });
    });
}


setInterval(() => {
    makeRequest();
}, 500);