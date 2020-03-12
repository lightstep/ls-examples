FROM python:3.7
RUN pip install git+https://github.com/lightstep/ls-trace-py.git@codeboten/metricsingest
ADD client.py /app/client.py
CMD ["ls-trace-run", "/usr/local/bin/python", "/app/client.py"]
