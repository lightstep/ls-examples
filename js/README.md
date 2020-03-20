# js examples

## Environment variables

Export or add to a .env file

```bash
export LIGHTSTEP_ACCESS_TOKEN=<lightstep access token>
```

optionally, set the lightstep host

```bash
export LIGHTSTEP_HOST=ingest.staging.lightstep.com
```

## Start the client

```bash
docker-compose up
```

## Supported variables

| Name                     | Required | Default              |
| ------------------------ | -------- | -------------------- |
| LIGHTSTEP_ACCESS_TOKEN   | yes      |
| LIGHTSTEP_COMPONENT_NAME | yes      |
| LIGHTSTEP_HOST           | No       | ingest.lightstep.com |
