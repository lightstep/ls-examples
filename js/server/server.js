'use strict';

const LIGHTSTEP_ACCESS_TOKEN = process.env.LIGHTSTEP_ACCESS_TOKEN;
const COMPONENT_NAME =
  process.env.LIGHTSTEP_COMPONENT_NAME || 'ls-trace-js-server';
const PORT = process.env.PORT || 8080;
const LIGHTSTEP_HOST =
  process.env.LIGHTSTEP_HOST || 'https://ingest.lightstep.com';
const LIGHTSTEP_METRICS_URL = `${LIGHTSTEP_HOST}/metrics`;

const express = require('express');
const tracer = require('ls-trace').init({
  experimental: {
    b3: true,
  },
  clientToken: LIGHTSTEP_ACCESS_TOKEN,
  runtimeMetrics: true,
  reportingInterval: 30 * 1000,
  componentName: COMPONENT_NAME,
  url: LIGHTSTEP_HOST,
  metricsUrl: LIGHTSTEP_METRICS_URL,
  tags: `lightstep.service_name:${COMPONENT_NAME},lightstep.access_token:${LIGHTSTEP_ACCESS_TOKEN}`,
});

const app = express();
app.get('/', (req, res) => {
  res.send('running...');
});

app.get('/ping', (req, res) => {
  res.send('pong');
});

app.listen(PORT);
console.log(`Running on 8080`);
