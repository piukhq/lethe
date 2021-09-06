FROM ghcr.io/binkhq/python:3.9

WORKDIR /app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy --ignore-pipfile

COPY lethe /app/lethe

ENV PROMETHEUS_MULTIPROC_DIR=/dev/shm
ENTRYPOINT ["linkerd-await", "--"]
CMD [ "gunicorn", "--workers=2", "--threads=2", "--error-logfile=-", \
                  "--logger-class=app.GunicornLogger", \
                  "--access-logfile=-", "--bind=0.0.0.0:9000", \
                  "--bind=0.0.0.0:9100", "lethe:app" ]
