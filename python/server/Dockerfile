FROM python:3.7
RUN pip install git+https://github.com/lightstep/ls-trace-py.git@codeboten/metricsingest flask
ADD server.py /app/server.py
CMD ["ls-trace-run", "/usr/local/bin/python", "/app/server.py"]
