FROM python:3.10.6

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN apt-get update && apt-get install -y git curl && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./app /app
COPY ./worker-start.sh /worker-start.sh
WORKDIR /app
ENV PYTHONPATH=/app

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# running celery as root
ENV C_FORCE_ROOT=1

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
