FROM python:3.7
RUN pip install ls-trace
ADD client.py /app/client.py
CMD ["ls-trace-run", "/usr/local/bin/python", "/app/client.py"]
