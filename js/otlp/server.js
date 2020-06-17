'use strict';

const PORT = process.env.PORT || 8080;
const ACCESS_TOKEN = process.env.LIGHTSTEP_ACCESS_TOKEN;
const COMPONENT_NAME =
    process.env.LIGHTSTEP_COMPONENT_NAME || 'ls-trace-js-server';
const SERVICE_VERSION = process.env.LIGHTSTEP_SERVICE_VERSION || '0.0.1';

const tracer = require('./tracer')(COMPONENT_NAME);
// eslint-disable-next-line import/order
const http = require('http');

/** Starts a HTTP server that receives requests on sample server port. */
function startServer(port) {
    // Creates a server
    const server = http.createServer(handleRequest);
    // Starts the server
    server.listen(port, (err) => {
        if (err) {
            throw err;
        }
        console.log(`Node HTTP listening on ${port}`);
    });
}

/** A function which handles requests and send response. */
function handleRequest(request, response) {
    const currentSpan = tracer.getCurrentSpan();
    // display traceid in the terminal
    console.log(`traceid: ${currentSpan.context().traceId}`);
    const span = tracer.startSpan('handleRequest', {
        parent: currentSpan,
        kind: 1, // server
        attributes: { key: 'value' },
    });
    // Annotate our span to capture metadata about the operation
    span.addEvent('invoking handleRequest');
    try {
        const body = [];
        request.on('error', (err) => console.log(err));
        request.on('data', (chunk) => body.push(chunk));
        request.on('end', () => {
            // deliberately sleeping to mock some action.
            setTimeout(() => {
                span.end();
                response.end('Hello World!');
            }, 2000);
        });
    } catch (err) {
        console.error(err);
        span.end();
    }
}

startServer(PORT);