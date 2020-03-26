# python examples


## Install ls-trace-py
```bash
pip install git+https://github.com/lightstep/ls-trace-py.git@codeboten/metricsingest
```
## Export your access token
```bash
export SECRET_TOKEN=<lightstep access token>
```

## Start the client

```bash
LIGHTSTEP_ACCESS_TOKEN=${SECRET_TOKEN} \
LIGHTSTEP_COMPONENT_NAME=demo-python \
LIGHTSTEP_SERVICE_VERSION=0.0.8 \
ls-trace-run python client.py
```

## Supported variables


| Name | Required | Default |
| ---- | -------- | ------- |
|LIGHTSTEP_ACCESS_TOKEN| yes|
|LIGHTSTEP_COMPONENT_NAME|yes|
|LIGHTSTEP_SERVICE_VERSION|yes|
|LIGHTSTEP_HOST| No | ingest.lightstep.com|
|LIGHTSTEP_PORT| No | 443 |
|LIGHTSTEP_SECURE| No | 1 |