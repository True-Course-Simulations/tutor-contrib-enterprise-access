# syntax=docker/dockerfile:1

FROM python:3.12-slim

USER root

# System deps commonly needed by Django + psycopg/mysqlclient + building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc g++ make \
    curl \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
  && rm -rf /var/lib/apt/lists/*

ARG ENTERPRISE_ACCESS_REPO={{ ENTERPRISE_ACCESS_REPO }}
ARG ENTERPRISE_ACCESS_VERSION={{ OPENEDX_COMMON_VERSION }}

ENV ENTERPRISE_ACCESS_APP_DIR=/openedx/enterprise-access
WORKDIR ${ENTERPRISE_ACCESS_APP_DIR}

# Get the app code
RUN git clone --depth 1 --branch ${ENTERPRISE_ACCESS_VERSION} ${ENTERPRISE_ACCESS_REPO} . \
 || (git clone --depth 1 ${ENTERPRISE_ACCESS_REPO} . && git checkout ${ENTERPRISE_ACCESS_VERSION})

# Create and use a dedicated venv (recommended)
RUN python -m venv /openedx/venv
ENV PATH="/openedx/venv/bin:${PATH}"

# Copy Tutor settings override
COPY ./settings/tutor.py ${ENTERPRISE_ACCESS_APP_DIR}/enterprise_access/settings/tutor.py

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements/production.txt \
 && pip install --no-cache-dir django-log-request-id django-redis

ENV DJANGO_SETTINGS_MODULE=enterprise_access.settings.tutor

EXPOSE 8000

# Run gunicorn from the venv (python 3.12)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "enterprise_access.wsgi:application"]
