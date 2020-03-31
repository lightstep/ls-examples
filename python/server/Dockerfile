FROM python:3.7
RUN pip install flask ls-trace
ADD server.py /app/server.py
CMD ["ls-trace-run", "/usr/local/bin/python", "/app/server.py"]
