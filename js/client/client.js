'use strict';

const LIGHTSTEP_ACCESS_TOKEN = process.env.LIGHTSTEP_ACCESS_TOKEN;
const COMPONENT_NAME =
  process.env.LIGHTSTEP_COMPONENT_NAME || 'ls-trace-js-client';
const TARGET_URL = process.env.TARGET_URL || 'http://localhost:8080/ping';
const LIGHTSTEP_HOST = process.env.LIGHTSTEP_HOST || 'ingest.lightstep.com';
const LIGHTSTEP_URL = `https://${LIGHTSTEP_HOST}`;
const LIGHTSTEP_METRICS_URL = `${LIGHTSTEP_URL}/metrics`;

const tracer = require('ls-trace').init({
  experimental: {
    b3: true,
  },
  clientToken: LIGHTSTEP_ACCESS_TOKEN,
  runtimeMetrics: true,
  reportingInterval: 30 * 1000,
  componentName: COMPONENT_NAME,
  url: LIGHTSTEP_URL,
  metricsUrl: LIGHTSTEP_METRICS_URL,
  tags: `lightstep.service_name:${COMPONENT_NAME},lightstep.access_token:${LIGHTSTEP_ACCESS_TOKEN}`,
});
const scope = tracer.scope();

const http = require('http');

setInterval(() => {
  const span = tracer.startSpan('client.ping');
  console.log('send: ping');
  scope.activate(span, () => {
    http.get(TARGET_URL, resp => {
      let data = '';
      resp.on('data', chunk => (data += chunk));
      resp.on('end', () => console.log(`recv: ${data}`));
      resp.on('error', err => console.log('Error: ' + err.message));
    });
  });
  span.finish();
}, 500);
