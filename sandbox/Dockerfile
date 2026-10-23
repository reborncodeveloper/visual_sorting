FROM python:3.12-alpine

WORKDIR /work
RUN adduser -D -u 10001 sandbox
USER sandbox

COPY runner.py /work/runner.py

CMD ["python", "/work/runner.py"]